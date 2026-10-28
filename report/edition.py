#!/usr/bin/env python3
"""Edition-specific numbers and figures for the weekly briefing (run after analyze.py).

Writes out/edition.json (every number the briefing cites that analyze.py does not compute),
out/tables/edition_*.md and out/figures/fig_weekly.png, fig_disclosure.png.
Every value is derived from the snapshot database, pairs/version_pairs.json, the
classifications and out/results.json, so a reviewer can re-run this file to check them.
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# Palette, rcParams and helpers copied from analyze.py (importing it would re-run the whole analysis).
PAL = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
       "magenta": "#e87ba4", "green": "#008300", "violet": "#4a3aa7", "red": "#e34948"}
GREY, INK, INK2 = "#b8b7b1", "#0b0b0b", "#52514e"
plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.5, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 150, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "font.family": "sans-serif",
})


def parse_ts(s):
    s = s.replace("Z", "+00:00")
    if re.match(r"^\d{4}-\d\d-\d\d$", s):
        return dt.datetime.fromisoformat(s).replace(tzinfo=dt.UTC)
    t = dt.datetime.fromisoformat(s)
    return (t if t.tzinfo else t.replace(tzinfo=dt.UTC)).astimezone(dt.UTC)


def days(a, b):
    return (b - a).total_seconds() / 86400.0

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIG = os.path.join(OUT, "figures")
TAB = os.path.join(OUT, "tables")
REPO = os.path.dirname(HERE)
LAST_EDITION_SNAPSHOT = "2026-10-24T06:21:17Z"   # published/meta.json of the 2026-10-25 edition
TOP_HOST = "openai.com"
STREAK_START = "2026-10-02"

R = json.load(open(os.path.join(OUT, "results.json")))
c = sqlite3.connect("file:" + os.path.join(HERE, "data", "docs.sqlite.snapshot") + "?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: [dict(r) for r in c.execute(s, a)]  # noqa: E731

E: dict = {"last_edition_snapshot": LAST_EDITION_SNAPSHOT, "snapshot_ts": R["snapshot_ts"]}

# ---------------------------------------------------------------- pairs in the window
pairs = json.load(open(os.path.join(HERE, "pairs", "version_pairs.json")))
cls = {}
for f in sorted(glob.glob(os.path.join(HERE, "classifications", "batch_*.json"))):
    for r in json.load(open(f)):
        cls[(r["slug"], int(r["version"]))] = r
for o in json.load(open(os.path.join(HERE, "classifications", "overrides.json"))):
    r = cls.get((o["slug"], int(o["version"])))
    if r:
        r["category"] = o["category"]
        for fl in ("score_change", "license_change", "safety_related", "model_scope_change", "correction"):
            r[fl] = bool(o.get("flags", {}).get(fl, False))
app_by_ver = {(a["slug"], a["version"]): a for a in R["appendix_rows"]}
SUB = {"content_minor", "content_major", "replacement"}
migr = {(a["slug"], a["version"]) for a in []}
window = [p for p in pairs if p["fetched"] > LAST_EDITION_SNAPSHOT]
E["window_pairs"] = len(window)
wc = collections.Counter(cls[(p["slug"], p["version"])]["category"] for p in window)
E["window_by_category"] = dict(wc)
E["window_substantive"] = sum(wc[k] for k in SUB)
E["window_safety_related"] = sum(1 for p in window if cls[(p["slug"], p["version"])].get("safety_related")
                                 and cls[(p["slug"], p["version"])]["category"] in SUB)
E["window_hf_furniture"] = sum(1 for p in window if cls[(p["slug"], p["version"])]["category"] == "furniture"
                               and "huggingface.co" in p["url"])
E["window_extraction_noise"] = wc["extraction_noise"]
E["window_appendix_ids"] = [app_by_ver[(p["slug"], p["version"])]["id"] for p in window
                            if (p["slug"], p["version"]) in app_by_ver]
E["window_versions"] = len(q("SELECT id FROM document_versions WHERE fetched_at > ?", LAST_EDITION_SNAPSHOT))

# ---------------------------------------------------------------- new documents in the window
new_docs = q("SELECT slug, title, publisher, doc_type, publication_date, first_seen, source_of_lead, canonical_url "
             "FROM documents WHERE first_seen > ? AND status != 'removed' ORDER BY first_seen", LAST_EDITION_SNAPSHOT)
E["new_docs"] = len(new_docs)
rows = []
for d in new_docs:
    lag = days(parse_ts(d["publication_date"]), parse_ts(d["first_seen"])) if d["publication_date"] else float("nan")
    rows.append((d["first_seen"][:10], d["publisher"].replace("_", " "), d["doc_type"].replace("_", " "),
                 f"[{d['title'][:58] + ('...' if len(d['title']) > 58 else '')}](https://systemcards.org/docs/{d['slug']}.html)",
                 d["publication_date"] or "", f"{lag:.0f}" if lag == lag else "n/a", d["source_of_lead"].replace("_", " ")))
E["new_docs_lag_median"] = float(np.median([days(parse_ts(d["publication_date"]), parse_ts(d["first_seen"]))
                                            for d in new_docs if d["publication_date"]]))
open(os.path.join(TAB, "edition_new_docs.md"), "w").write(
    "| Tracked since | Publisher | Type | Document | Published | Lag (days) | Lead source |\n|---|---|---|---|---|---|---|\n"
    + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows) + "\n")

# ---------------------------------------------------------------- runs in the window + blocking
runs_w = [r for r in R["runs"] if r["ts"] > LAST_EDITION_SNAPSHOT]
E["window_runs"] = len(runs_w)
E["window_outage_runs"] = sum(1 for r in runs_w if r["outage"])
E["window_agent_failed"] = sum(1 for r in runs_w if r["agent_failed"])
E["window_blocked_per_run"] = [r["blocked"] for r in runs_w]
E["window_fp_checks"] = sum(r["fp_n"] for r in runs_w)
E["window_fp_changed"] = sum(r["fp_changed"] for r in runs_w)
last_run = R["runs"][-1]["run_id"]
blocked_last = q("SELECT d.canonical_url, d.doc_type FROM link_checks l JOIN documents d ON d.id=l.document_id "
                 "WHERE l.run_id=? AND l.check_type='link' AND l.outcome='blocked'", last_run)
E["blocked_last_run"] = len(blocked_last)
E["blocked_last_run_by_host"] = dict(collections.Counter(re.sub(r"^https?://([^/]+).*$", r"\1", b["canonical_url"]) for b in blocked_last))
E["blocked_last_run_by_type"] = dict(collections.Counter(b["doc_type"] for b in blocked_last))
# content re-fetches of the blocked host during the probe-blocked streak
fp_host = q("SELECT l.outcome, l.http_status FROM link_checks l JOIN documents d ON d.id=l.document_id "
            "WHERE l.check_type='fingerprint' AND l.ts >= ? AND d.canonical_url LIKE ?", STREAK_START, f"https://{TOP_HOST}/%")
E["streak_host"] = TOP_HOST
E["streak_since"] = R["top_host_all_blocked_since"]
E["streak_days"] = R["top_host_all_blocked_days"]
E["streak_fp_outcomes"] = dict(collections.Counter(x["outcome"] for x in fp_host))
E["streak_fp_status"] = dict(collections.Counter(str(x["http_status"]) for x in fp_host))
E["runs_since_last_outage"] = R["n_runs_since_last_outage"]
E["last_outage_date"] = R["last_outage_date"]

# ---------------------------------------------------------------- raw captures available on this host
vers = q("SELECT id, fetched_at, raw_path FROM document_versions ORDER BY id")
missing = [v for v in vers if not os.path.exists(os.path.join(REPO, v["raw_path"]))]
E["versions_total"] = len(vers)
E["versions_raw_missing"] = len(missing)
E["versions_raw_missing_first_date"] = min(v["fetched_at"] for v in missing)[:10] if missing else ""
E["versions_raw_missing_since_window"] = sum(1 for v in missing if v["fetched_at"] > LAST_EDITION_SNAPSHOT)
# the monitor's own raw-capture check (change_summary = "Extractor drift: ...")
drift = q("SELECT ts FROM changelog WHERE action='field_update' AND detail LIKE '%Deleted lines found verbatim in the new raw capture%' ORDER BY ts")
E["monitor_drift_checks"] = len(drift)
E["monitor_drift_first"] = drift[0]["ts"][:10] if drift else ""
E["monitor_drift_window"] = sum(1 for d in drift if d["ts"] > LAST_EDITION_SNAPSHOT)

# ---------------------------------------------------------------- disclosure rule over all substantive changes
MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? \d{1,2}(?!\d)(?:,? \d{4})?"   # month + day, not "August 2026"
# A note that describes the change and carries a date. A bare "last updated" stamp or an arXiv
# submission history is not counted: it dates the revision without saying what changed.
DATED = re.compile(r"change[ -]?log|\bdated\b|errat|update note|revision note|correction note|"
                   rf"(?:update|correction|revision|notice)[^.;]{{0,25}}{MONTH}|{MONTH}[^.;]{{0,15}}(?:update|correction|revision|notice)|"
                   r"notice[^.;]{0,40}\d{1,2}/\d{1,2}/\d{4}", re.I)
SILENT = re.compile(r"silent|quietly|no change ?log|without (a |any )?(revision )?not(e|ice)|no erratum|undisclosed|no note", re.I)


def disclosure(a):
    txt = a["summary"] + " " + a["notable"]
    if DATED.search(a["summary"]) and not re.search(r"no change ?log|without", a["summary"], re.I):
        return "dated note"
    if SILENT.search(txt):
        return "called silent"
    return "no note mentioned"


disc = collections.Counter(disclosure(a) for a in R["appendix_rows"])
E["disclosure_counts"] = dict(disc)
E["disclosure_n"] = len(R["appendix_rows"])
by_pub = collections.defaultdict(collections.Counter)
for a in R["appendix_rows"]:
    by_pub[a["publisher"]][disclosure(a)] += 1
E["disclosure_by_publisher"] = {k: dict(v) for k, v in by_pub.items()}
E["disclosure_dated_ids"] = [a["id"] for a in R["appendix_rows"] if disclosure(a) == "dated note"]
E["disclosure_silent_ids"] = [a["id"] for a in R["appendix_rows"] if disclosure(a) == "called silent"]
pubs = sorted(by_pub, key=lambda k: -sum(by_pub[k].values()))
open(os.path.join(TAB, "edition_disclosure.md"), "w").write(
    "| Publisher | Substantive changes | Summary mentions a dated note | Summary calls the edit silent | Neither |\n|---|---|---|---|---|\n"
    + "\n".join(f"| {k.replace('_', ' ')} | {sum(by_pub[k].values())} | {by_pub[k]['dated note']} | {by_pub[k]['called silent']} | {by_pub[k]['no note mentioned']} |"
                for k in pubs if sum(by_pub[k].values()) >= 3)
    + f"\n| all publishers | {len(R['appendix_rows'])} | {disc['dated note']} | {disc['called silent']} | {disc['no note mentioned']} |\n")

# ---------------------------------------------------------------- this week's substantive changes table
rows = []
for p in sorted(window, key=lambda p: (p["fetched"], p["slug"])):
    a = app_by_ver.get((p["slug"], p["version"]))
    if not a:
        continue
    fl = ", ".join(f.replace("_change", "").replace("_related", "").replace("model_scope", "scope") for f in a["flags"])
    rows.append((a["id"], a["detected"], a["publisher"].replace("_", " "),
                 f"[{a['title'][:50] + ('...' if len(a['title']) > 50 else '')}](https://systemcards.org/docs/{a['slug']}.html)",
                 f"v{a['prev_version']}→v{a['version']}", a["category"].replace("content_", "") + (f" ({fl})" if fl else ""),
                 a["summary"].replace("|", "\\|")))
open(os.path.join(TAB, "edition_changes.md"), "w").write(
    "| Id | Detected | Publisher | Document | Versions | Category (flags) | What changed (classifier summary) |\n|---|---|---|---|---|---|---|\n"
    + "\n".join("| " + " | ".join(r) + " |" for r in rows) + "\n")

# ---------------------------------------------------------------- figure: weekly mix of detected version changes
CAT_ORDER = ["furniture", "extraction_noise", "metadata_minor", "content_minor", "content_major", "replacement"]
CAT_COL = {"furniture": GREY, "extraction_noise": "#d9d8d2", "metadata_minor": PAL["yellow"],
           "content_minor": PAL["aqua"], "content_major": PAL["blue"], "replacement": PAL["red"]}
CAT_LAB = {"furniture": "page furniture", "extraction_noise": "extraction noise", "metadata_minor": "metadata / typo",
           "content_minor": "content: minor", "content_major": "content: major", "replacement": "replaced / gone"}
mig = set()
# tracker migrations: analyze.py marks them in results via cat 'tracker_migration' in appendix exclusion; recompute by
# the same rule it exposes: any classified pair absent from publisher-side counts. Simplest: re-derive from results.
# results.json does not list migration pairs, so rebuild the rule here (content type changed or canonical_url update inside the interval).
vt = {v["id"]: v["content_type"] for v in q("SELECT id, content_type FROM document_versions")}
url_upd = collections.defaultdict(list)
doc_id = {d["slug"]: d["id"] for d in q("SELECT id, slug FROM documents")}
for cl in q("SELECT document_id, ts, detail FROM changelog WHERE action='field_update'"):
    if json.loads(cl["detail"]).get("field") == "canonical_url":
        url_upd[cl["document_id"]].append(cl["ts"])
canon = {d["id"]: d["canonical_url"] for d in q("SELECT id, canonical_url FROM documents")}


def _same_article(a: str, b: str) -> bool:   # as in analyze.py: a slug rename of the same article id
    strip = lambda u: re.sub(r"/(\d{5,})-[^/]*/?$", r"/\1", u.split("?")[0])  # noqa: E731
    return strip(a) == strip(b) and re.search(r"/\d{5,}-[^/]*/?$", a.split("?")[0]) is not None


for cl in q("SELECT document_id, ts, detail FROM changelog WHERE action='status_change'"):
    d = json.loads(cl["detail"])
    if d.get("new") == "moved":
        to = re.sub(r"^.*redirects to ", "", d.get("justification", "")).strip().rstrip(".")
        if not _same_article(canon[cl["document_id"]], to):
            url_upd[cl["document_id"]].append(cl["ts"])
def is_migration(p):
    a, b = parse_ts(p["prev_fetched"]), parse_ts(p["fetched"])
    return vt[p["prev_version"]] != vt[p["version"]] or any(
        (parse_ts(t) - a).total_seconds() > 60 and (parse_ts(t) - b).total_seconds() <= 60 for t in url_upd[doc_id[p["slug"]]])
pub_pairs = [p for p in pairs if not is_migration(p)]
E["n_pub_pairs_recomputed"] = len(pub_pairs)   # should equal results.json n_pub_pairs (437) up to the slug-rename exception
weeks = collections.defaultdict(collections.Counter)
for p in pub_pairs:
    d = parse_ts(p["fetched"]).date()
    wk = d - dt.timedelta(days=d.weekday())
    weeks[wk][cls[(p["slug"], p["version"])]["category"]] += 1
wks = sorted(weeks)
fig, ax = plt.subplots(figsize=(6.8, 2.4))
bottom = np.zeros(len(wks))
for k in CAT_ORDER:
    vals = np.array([weeks[w][k] for w in wks])
    ax.bar(range(len(wks)), vals, bottom=bottom, color=CAT_COL[k], width=0.72, lw=0, label=CAT_LAB[k])
    bottom += vals
ax.set_xticks(range(len(wks)))
ax.set_xticklabels([w.strftime("%d %b") for w in wks], fontsize=6.5)
ax.set_xlabel("week of detection (Monday)")
ax.set_ylabel("stored version changes")
ax.axvline(wks.index(dt.date(2026, 8, 31)) - 0.5, color=PAL["red"], lw=0.8, ls="--")
ax.text(wks.index(dt.date(2026, 8, 31)) - 0.4, bottom.max() * 0.97, "furniture filter\nrecomputed", fontsize=6, color=PAL["red"], va="top")
ax.text(len(wks) - 1, bottom[-1] + 1.5, "this edition\n(3 days)", fontsize=6, color=INK2, ha="center")
ax.set_ylim(0, bottom.max() * 1.15)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=6, handlelength=1, columnspacing=0.8)
fig.savefig(os.path.join(FIG, "fig_weekly.png"), dpi=170)
plt.close(fig)
E["weekly"] = {w.isoformat(): dict(weeks[w]) for w in wks}
E["weekly_substantive"] = {w.isoformat(): sum(weeks[w][k] for k in SUB) for w in wks}

# ---------------------------------------------------------------- figure: disclosure by publisher
DISC_COL = {"dated note": PAL["blue"], "called silent": PAL["orange"], "no note mentioned": GREY}
DISC_LAB = {"dated note": "classifier summary mentions a dated change log or update note",
            "called silent": "classifier summary calls the edit silent or undisclosed",
            "no note mentioned": "neither (unknown)"}
top = [k for k in pubs if sum(by_pub[k].values()) >= 3]
fig, ax = plt.subplots(figsize=(6.8, 2.4))
left = np.zeros(len(top))
for k in ("dated note", "called silent", "no note mentioned"):
    vals = np.array([by_pub[pb][k] for pb in top])
    ax.barh(range(len(top)), vals, left=left, color=DISC_COL[k], height=0.68, lw=0, label=DISC_LAB[k])
    left += vals
ax.set_yticks(range(len(top)))
ax.set_yticklabels([f"{pb.replace('_', ' ')} (n={sum(by_pub[pb].values())})" for pb in top], fontsize=6.5)
ax.invert_yaxis()
ax.set_xlabel("substantive publisher-side changes since 11 Aug 2026")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=1, handlelength=1)
fig.savefig(os.path.join(FIG, "fig_disclosure.png"), dpi=170)
plt.close(fig)

json.dump(E, open(os.path.join(OUT, "edition.json"), "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in E.items() if k not in ("weekly",)}, indent=1, default=str))
