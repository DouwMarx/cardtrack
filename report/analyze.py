#!/usr/bin/env python3
"""Compute every number, table and figure used by the report from the data snapshot.

Inputs (all under data/ and pairs/, produced by snapshot.sh and build_pairs.py, plus
classifications/*.json written by the classification sub-agents):
  data/docs.sqlite.snapshot   the cardtrack database
  data/runlogs/run-*.log      daily run logs (agent phase status)
  data/journal_events.json    host suspend/resume + service start events (optional)
  data/candidates.json        current Phase A candidate queue (optional)
  pairs/version_pairs.json    version-pair manifest
  classifications/*.json      sub-agent classifications of version pairs

Outputs (under out/): results.json, macros.tex, tables/*.tex, figures/*.pdf,
comprehensive_report.md. The LaTeX report only \\input's these; nothing is typed by hand.
"""
import collections
import datetime as dt
import glob
import json
import math
import os
import re
import sqlite3
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")
FIG = os.path.join(OUT, "figures")
TAB = os.path.join(OUT, "tables")
for d in (OUT, FIG, TAB):
    os.makedirs(d, exist_ok=True)

FILTER_RECOMPUTE = "2026-08-31T08:40:00Z"   # furniture-aware fingerprint recompute run (08:41-10:13Z)
BACKFILL_END = "2026-08-11"       # first_seen before this = supervised backfill, not discovery

# ---- validated categorical palette (dataviz skill reference instance, light mode) ----
PAL = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
       "magenta": "#e87ba4", "green": "#008300", "violet": "#4a3aa7", "red": "#e34948"}
CAT = [PAL[k] for k in ("blue", "orange", "aqua", "yellow", "magenta", "green", "violet", "red")]
GREY = "#b8b7b1"
INK = "#0b0b0b"
INK2 = "#52514e"
plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.5, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 150, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42, "font.family": "sans-serif",
})


# ------------------------------------------------------------------ helpers
def parse_ts(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    if re.match(r"^\d{4}-\d\d-\d\d$", s):
        return dt.datetime.fromisoformat(s).replace(tzinfo=dt.UTC)
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.UTC)
    return t.astimezone(dt.UTC)


def days(a, b):
    return (b - a).total_seconds() / 86400.0


def pct(x, n):
    return 100.0 * x / n if n else float("nan")


def fmt(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if math.isnan(v):
            return "n/a"
        if abs(v) >= 100:
            return f"{v:,.0f}"
        if abs(v) >= 10:
            return f"{v:.1f}"
        return f"{v:.2f}" if abs(v) < 1 else f"{v:.1f}"
    return str(v)


def texesc(s):
    s = str(s).replace("\\quad", "\x00QUAD").replace("\\%", "\x00PCT")
    s = (s.replace("\\", "/").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")
         .replace("#", "\\#").replace("$", "\\$").replace("~", "\\textasciitilde{}"))
    return s.replace("\x00QUAD", "\\quad").replace("\x00PCT", "\\%")


def pretty(name):
    return {"model_card": "model card", "system_card": "system card",
            "independent_eval": "independent evaluation", "access_policy": "access policy",
            "addendum": "addendum", "other": "other", "text/html": "HTML", "application/pdf": "PDF",
            "open_weight_permissive": "open weight (permissive)",
            "open_weight_restrictive": "open weight (restrictive)", "closed": "closed",
            "restricted": "restricted", None: "unset"}.get(name, str(name).replace("_", " "))


# ------------------------------------------------------------------ load
c = sqlite3.connect("file:" + os.path.join(DATA, "docs.sqlite.snapshot") + "?mode=ro", uri=True)
c.row_factory = sqlite3.Row


def q(s, *a):
    return [dict(r) for r in c.execute(s, a)]


docs = q("SELECT * FROM documents ORDER BY id")
versions = q("SELECT * FROM document_versions ORDER BY document_id, fetched_at, id")
changelog = q("SELECT * FROM changelog ORDER BY ts, id")
checks = q("SELECT * FROM link_checks ORDER BY id")
index_links = q("SELECT * FROM index_links")
snapshot_ts = max([parse_ts(x["ts"]) for x in checks] + [parse_ts(x["ts"]) for x in changelog])
doc_by_id = {d["id"]: d for d in docs}
for d in docs:
    d["first_seen_ts"] = parse_ts(d["first_seen"])
    d["pub_ts"] = parse_ts(d["publication_date"]) if d["publication_date"] else None
for cl in changelog:
    try:
        cl["d"] = json.loads(cl["detail"])
    except Exception:
        cl["d"] = {}
R: dict = {"snapshot_ts": snapshot_ts.isoformat(), "snapshot_date": snapshot_ts.date().isoformat()}
tracked = [d for d in docs if d["status"] != "removed"]

# ------------------------------------------------------------------ 1. corpus
R["n_docs_ever"] = len(docs)
R["n_tracked"] = len(tracked)
R["n_removed"] = sum(1 for d in docs if d["status"] == "removed")
R["n_active"] = sum(1 for d in docs if d["status"] == "active")
R["n_moved"] = sum(1 for d in docs if d["status"] == "moved")
R["n_dead"] = sum(1 for d in docs if d["status"] == "dead")
R["n_versions"] = len(versions)
R["n_checks"] = len(checks)
R["n_changelog"] = len(changelog)
R["n_index_links"] = len(index_links)
R["n_publishers"] = len({d["publisher"] for d in tracked})
R["by_doc_type"] = collections.Counter(d["doc_type"] for d in tracked).most_common()
R["by_publisher"] = collections.Counter(d["publisher"] for d in tracked).most_common()
R["by_openness"] = collections.Counter(d["openness"] for d in tracked).most_common()
R["by_content_type"] = collections.Counter(
    next((v["content_type"] for v in reversed(versions) if v["document_id"] == d["id"]), None)
    for d in tracked).most_common()
R["share_pdf"] = pct(dict(R["by_content_type"]).get("application/pdf", 0), len(tracked))
R["share_safety_evals"] = pct(sum(1 for d in tracked if d["safety_evals"] == 1), len(tracked))
R["share_independent"] = pct(sum(1 for d in tracked if d["is_independent"]), len(tracked))
R["risk_domains"] = collections.Counter(
    x for d in tracked for x in json.loads(d["risk_domains"])).most_common()
R["pub_month"] = sorted(collections.Counter(
    (d["publication_date"] or "")[:7] for d in tracked if d["publication_date"]).items())
R["pub_date_min"] = min(d["publication_date"] for d in tracked if d["publication_date"])
R["pub_date_max"] = max(d["publication_date"] for d in tracked if d["publication_date"])
R["first_seen_min"] = min(d["first_seen"] for d in docs)[:10]
R["first_seen_max"] = max(d["first_seen"] for d in docs)[:10]
R["tracking_days"] = days(parse_ts(R["first_seen_min"]), snapshot_ts)
R["n_backfill"] = sum(1 for d in docs if d["first_seen"] < BACKFILL_END)
R["n_post_backfill"] = sum(1 for d in docs if d["first_seen"] >= BACKFILL_END)
R["n_docs_multi_version"] = sum(1 for d in tracked
                                if sum(1 for v in versions if v["document_id"] == d["id"]) > 1)
R["share_docs_multi_version"] = pct(R["n_docs_multi_version"], len(tracked))
R["max_versions"] = max(collections.Counter(v["document_id"] for v in versions).values())

# ------------------------------------------------------------------ 2. runs
run_re = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\dZ-local$")
runs: dict[str, dict] = {}
for ch in checks:
    if not run_re.match(ch["run_id"]):
        continue
    r = runs.setdefault(ch["run_id"], {"run_id": ch["run_id"], "link": collections.Counter(), "fingerprint": collections.Counter(),
                                       "ts": ch["ts"]})
    r["ts"] = min(r["ts"], ch["ts"])
    r[ch["check_type"]][ch["outcome"]] += 1
# run logs: agent phase
agent_status: dict[str, dict] = {}
for path in sorted(glob.glob(os.path.join(DATA, "runlogs", "run-*.log"))):
    txt = open(path, errors="replace").read()
    m = re.search(r"== cardtrack run (\S+) ", txt)
    if not m:
        continue
    rid = m.group(1)
    failed = ("agent exited" in txt) or ("AGENT PHASE FAILED" in txt)
    reason = ""
    if failed:
        if "error connecting to api.github.com" in txt or "MONITOR OUTAGE" in txt:
            reason = "network"
        elif "OAuth" in txt or "Failed to authenticate" in txt:
            reason = "auth"
        elif "No response from API" in txt:
            reason = "api"
        else:
            reason = "other"
    agent_status[rid] = {"failed": failed, "reason": reason,
                         "push_failed": "push failed" in txt,
                         "outage_flag": "MONITOR OUTAGE" in txt}
    mj = re.search(r'^\{"run_id".*\}$', txt, re.M)
    if mj:
        try:
            agent_status[rid]["monitor"] = json.loads(mj.group(0))
        except Exception:
            pass
# journal
journal = []
jp = os.path.join(DATA, "journal_events.json")
if os.path.exists(jp):
    journal = [{"ts": parse_ts(e["ts"]), "kind": e["kind"]} for e in json.load(open(jp))]
resumes = sorted(e["ts"] for e in journal if e["kind"] == "resume")
starts = sorted(e["ts"] for e in journal if e["kind"] == "service_start")
adds_by_run = collections.Counter(cl["run_id"] for cl in changelog if cl["action"] == "add")
newv_by_run = collections.Counter(cl["run_id"] for cl in changelog if cl["action"] == "new_version")
run_rows = []
for rid, r in sorted(runs.items(), key=lambda kv: kv[1]["ts"]):
    t = parse_ts(r["ts"])
    n_link = sum(r["link"].values())
    err = r["link"].get("error", 0)
    ok = r["link"].get("ok", 0) + r["link"].get("redirect_permanent", 0)
    outage = n_link > 0 and err == n_link
    partial = (not outage) and err > 0
    st = next((s for s in starts if abs((s - t).total_seconds()) < 240), None)
    last_resume = max((x for x in resumes if x <= (st or t)), default=None)
    since_resume = (st or t) - last_resume if last_resume else None
    a = agent_status.get(rid, {})
    run_rows.append({
        "run_id": rid, "ts": r["ts"], "date": r["ts"][:10], "n_link": n_link, "ok": ok,
        "blocked": r["link"].get("blocked", 0), "not_found": r["link"].get("not_found", 0),
        "redirect": r["link"].get("redirect_permanent", 0), "error": err,
        "fp_changed": r["fingerprint"].get("changed", 0), "fp_unchanged": r["fingerprint"].get("unchanged", 0),
        "fp_error": r["fingerprint"].get("error", 0), "fp_n": sum(r["fingerprint"].values()),
        "outage": outage, "partial": partial,
        "sec_since_resume": since_resume.total_seconds() if since_resume is not None else None,
        "resume_triggered": (since_resume is not None and since_resume.total_seconds() <= 120),
        # no run log copied for this run: agent phase unknown (not counted as healthy)
        "agent_known": bool(a), "agent_failed": a.get("failed", False), "agent_reason": a.get("reason", ""),
        "push_failed": a.get("push_failed", False), "adds": adds_by_run.get(rid, 0),
        "new_versions": newv_by_run.get(rid, 0),
        "candidates": (a.get("monitor") or {}).get("candidates"),
    })
R["runs"] = run_rows
R["n_runs"] = len(run_rows)
R["n_outage_runs"] = sum(1 for r in run_rows if r["outage"])
R["n_partial_runs"] = sum(1 for r in run_rows if r["partial"])
R["n_valid_runs"] = R["n_runs"] - R["n_outage_runs"]
R["share_outage_runs"] = pct(R["n_outage_runs"], R["n_runs"])
R["n_resume_triggered_outages"] = sum(1 for r in run_rows if r["outage"] and r["resume_triggered"])
R["n_resume_triggered_runs"] = sum(1 for r in run_rows if r["resume_triggered"])
R["n_resume_triggered_valid"] = sum(1 for r in run_rows if r["resume_triggered"] and not r["outage"])
R["n_outages_not_resume"] = sum(1 for r in run_rows if r["outage"] and not r["resume_triggered"])
R["n_journal_matched_runs"] = sum(1 for r in run_rows if r["sec_since_resume"] is not None)
R["n_agent_failed_runs"] = sum(1 for r in run_rows if r["agent_failed"])
R["n_agent_auth_failed"] = sum(1 for r in run_rows if r["agent_reason"] == "auth")
R["n_agent_failed_on_outage"] = sum(1 for r in run_rows if r["agent_failed"] and r["outage"])
R["n_agent_failed_valid"] = sum(1 for r in run_rows if r["agent_failed"] and not r["outage"])
R["agent_fail_reasons"] = collections.Counter(r["agent_reason"] for r in run_rows if r["agent_failed"]).most_common()
R["n_push_failed"] = sum(1 for r in run_rows if r["push_failed"])
R["n_runs_with_adds"] = sum(1 for r in run_rows if r["adds"] > 0)
R["adds_daily_runs"] = sum(r["adds"] for r in run_rows)
R["n_fully_good_runs"] = sum(1 for r in run_rows if not r["outage"] and r["agent_known"] and not r["agent_failed"])
R["n_runs_agent_unknown"] = sum(1 for r in run_rows if not r["agent_known"])
R["n_runs_agent_known"] = R["n_runs"] - R["n_runs_agent_unknown"]
R["last_run_log_date"] = max((r["date"] for r in run_rows if r["agent_known"]), default="")
# recency: the last full outage and how many runs have been outage-free since
_out_ts = [r["ts"] for r in run_rows if r["outage"]]
R["last_outage_date"] = max(_out_ts)[:10] if _out_ts else ""
R["n_runs_since_last_outage"] = sum(1 for r in run_rows if not _out_ts or r["ts"] > max(_out_ts))
# longest outage streak
best = cur = 0
for r in run_rows:
    cur = cur + 1 if r["outage"] else 0
    best = max(best, cur)
R["longest_outage_streak"] = best
# expected daily runs vs actual
first_run, last_run = parse_ts(run_rows[0]["ts"]), parse_ts(run_rows[-1]["ts"])
R["calendar_days_span"] = int(days(first_run, last_run)) + 1
R["n_missing_days"] = R["calendar_days_span"] - len({r["date"] for r in run_rows})
R["median_sec_since_resume_outage"] = int(np.median(
    [r["sec_since_resume"] for r in run_rows if r["outage"] and r["sec_since_resume"] is not None]))
R["median_sec_since_resume_valid"] = int(np.median(
    [r["sec_since_resume"] for r in run_rows if not r["outage"]
     and r["sec_since_resume"] is not None] or [float("nan")]))
outage_runs = {r["run_id"] for r in run_rows if r["outage"]}

# ------------------------------------------------------------------ 3. availability (target side)
# Target-side availability: checks in non-outage runs whose probe reached a server (an HTTP status
# exists). Errors without a status are the fetcher's own failures (DNS, connection) and are
# counted separately as tracker-side.
valid_all = [ch for ch in checks if ch["check_type"] == "link" and run_re.match(ch["run_id"])
             and ch["run_id"] not in outage_runs]
R["n_tracker_errors_valid_runs"] = sum(1 for ch in valid_all if ch["http_status"] is None)
valid_link = [ch for ch in valid_all if ch["http_status"] is not None]
R["n_valid_link_checks"] = len(valid_link)
oc = collections.Counter(ch["outcome"] for ch in valid_link)
R["valid_link_outcomes"] = oc.most_common()
for k in ("ok", "blocked", "redirect_permanent", "not_found", "error"):
    R[f"share_link_{k}"] = pct(oc.get(k, 0), len(valid_link))
per_doc_outcomes: dict[int, list] = collections.defaultdict(list)
for ch in valid_link:
    per_doc_outcomes[ch["document_id"]].append(ch)
R["n_docs_with_valid_checks"] = len(per_doc_outcomes)
R["median_valid_checks_per_doc"] = float(np.median([len(v) for v in per_doc_outcomes.values()]))
ever = collections.Counter()
for did, lst in per_doc_outcomes.items():
    for o in {x["outcome"] for x in lst}:
        ever[o] += 1
R["docs_ever_blocked"] = ever.get("blocked", 0)
R["docs_ever_not_found"] = ever.get("not_found", 0)
R["docs_ever_redirect"] = ever.get("redirect_permanent", 0)
R["docs_ever_error_valid"] = ever.get("error", 0)
R["docs_always_ok"] = sum(1 for lst in per_doc_outcomes.values()
                          if all(x["outcome"] == "ok" for x in lst))
R["share_docs_always_ok"] = pct(R["docs_always_ok"], len(per_doc_outcomes))
blocked_hosts = collections.Counter()
blocked_docs_hosts = collections.Counter()
for did, lst in per_doc_outcomes.items():
    host = re.sub(r"^https?://([^/]+).*$", r"\1", doc_by_id[did]["canonical_url"])
    nb = sum(1 for x in lst if x["outcome"] == "blocked")
    blocked_hosts[host] += nb
    if nb:
        blocked_docs_hosts[host] += 1
R["blocked_by_host"] = blocked_hosts.most_common()
R["blocked_docs_by_host"] = blocked_docs_hosts.most_common()
# first blocked date per doc (are blocks persistent?)
blocked_persist = []
for did, lst in per_doc_outcomes.items():
    b = [x for x in lst if x["outcome"] == "blocked"]
    if b:
        after_first = [x for x in lst if x["ts"] >= b[0]["ts"]]
        blocked_persist.append(pct(len(b), len(after_first)))
R["blocked_persistence_median"] = float(np.median(blocked_persist)) if blocked_persist else float("nan")
R["first_blocked_date"] = min((x["ts"] for lst in per_doc_outcomes.values() for x in lst
                               if x["outcome"] == "blocked"), default="")[:10]
# moved docs
moved = [cl for cl in changelog if cl["action"] == "status_change" and cl["d"].get("new") == "moved"]
R["moved_events"] = [{"slug": cl["d"].get("slug"), "date": cl["ts"][:10],
                      "from": doc_by_id[cl["document_id"]]["canonical_url"],
                      "to": re.sub(r"^.*redirects to ", "", cl["d"].get("justification", ""))}
                     for cl in moved]
R["n_moved_events"] = len(moved)
R["n_removed_human"] = sum(1 for cl in changelog if cl["action"] == "status_change"
                           and cl["d"].get("new") == "removed" and cl["d"].get("actor") == "human")
R["n_removed_agent"] = sum(1 for cl in changelog if cl["action"] == "status_change"
                           and cl["d"].get("new") == "removed" and cl["d"].get("actor") == "agent")
# doc-days observed and event rates
doc_days = 0.0
for did, lst in per_doc_outcomes.items():
    doc_days += days(parse_ts(lst[0]["ts"]), parse_ts(lst[-1]["ts"]))
R["doc_days_observed"] = doc_days
R["doc_years_observed"] = doc_days / 365.25
R["moves_per_doc_year"] = R["n_moved_events"] / R["doc_years_observed"]
R["notfound_docs_per_doc_year"] = R["docs_ever_not_found"] / R["doc_years_observed"]
R["hard_loss_docs"] = R["docs_ever_not_found"] + R["n_dead"]
# staleness as of snapshot
stale = []
for d in tracked:
    lst = per_doc_outcomes.get(d["id"])
    if lst:
        stale.append(days(parse_ts(lst[-1]["ts"]), snapshot_ts))
R["staleness_median_days"] = float(np.median(stale))
R["staleness_max_days"] = float(np.max(stale))
R["docs_never_validly_checked"] = sum(1 for d in tracked if d["id"] not in per_doc_outcomes)

# ------------------------------------------------------------------ 4. discovery lag
lag_rows = []
for d in docs:
    if not d["pub_ts"]:
        continue
    lag = days(d["pub_ts"], d["first_seen_ts"])
    lag_rows.append({"slug": d["slug"], "publisher": d["publisher"], "doc_type": d["doc_type"],
                     "lead": d["source_of_lead"], "lag_days": lag,
                     "post_backfill": d["first_seen"] >= BACKFILL_END,
                     "published_in_window": d["publication_date"] >= BACKFILL_END,
                     "removed": d["status"] == "removed"})
live = [x for x in lag_rows if x["published_in_window"] and not x["removed"]]
catchup = [x for x in lag_rows if x["post_backfill"] and not x["published_in_window"]
           and not x["removed"]]
R["n_lag_live"] = len(live)
R["n_lag_catchup"] = len(catchup)
lags = np.array([x["lag_days"] for x in live]) if live else np.array([float("nan")])
R["lag_median_days"] = float(np.median(lags))
R["lag_mean_days"] = float(np.mean(lags))
R["lag_p75_days"] = float(np.percentile(lags, 75))
R["lag_p90_days"] = float(np.percentile(lags, 90))
R["lag_max_days"] = float(np.max(lags))
R["lag_share_within_1d"] = pct(int((lags <= 1).sum()), len(lags))
R["lag_share_within_3d"] = pct(int((lags <= 3).sum()), len(lags))
R["lag_share_within_7d"] = pct(int((lags <= 7).sum()), len(lags))
R["lag_by_lead"] = sorted(
    [(lead, len(g), float(np.median([x["lag_days"] for x in g])))
     for lead, g in collections.defaultdict(list, {
         k: [x for x in live if x["lead"] == k] for k in {x["lead"] for x in live}}).items()],
    key=lambda t: (-t[1], t[0]))
R["lag_by_type"] = sorted(
    [(t, len(g), float(np.median([x["lag_days"] for x in g])))
     for t, g in {k: [x for x in live if x["doc_type"] == k]
                  for k in {x["doc_type"] for x in live}}.items()], key=lambda t: -t[1])
R["catchup_median_age_days"] = float(np.median([x["lag_days"] for x in catchup])) if catchup else float("nan")
R["lead_share"] = collections.Counter(d["source_of_lead"] for d in tracked
                                       if d["first_seen"] >= BACKFILL_END).most_common()

# ------------------------------------------------------------------ 5. fingerprint checks / change hazard
fp_valid = [ch for ch in checks if ch["check_type"] == "fingerprint" and run_re.match(ch["run_id"])
            and ch["outcome"] in ("changed", "unchanged")]
R["n_fp_valid"] = len(fp_valid)
R["n_fp_changed"] = sum(1 for ch in fp_valid if ch["outcome"] == "changed")
R["share_fp_changed"] = pct(R["n_fp_changed"], len(fp_valid))
pre = [ch for ch in fp_valid if ch["ts"] < FILTER_RECOMPUTE]
post = [ch for ch in fp_valid if ch["ts"] >= FILTER_RECOMPUTE]
R["share_fp_changed_pre_filter"] = pct(sum(1 for ch in pre if ch["outcome"] == "changed"), len(pre))
R["share_fp_changed_post_filter"] = pct(sum(1 for ch in post if ch["outcome"] == "changed"), len(post))
R["n_fp_pre_filter"] = len(pre)
R["n_fp_post_filter"] = len(post)
# realized re-check interval: gaps between successive valid fingerprint observations per doc
obs: dict[int, list] = collections.defaultdict(list)
for v in versions:
    obs[v["document_id"]].append(parse_ts(v["fetched_at"]))
for ch in fp_valid:
    obs[ch["document_id"]].append(parse_ts(ch["ts"]))
gaps = []
for did, ts in obs.items():
    ts = sorted(ts)
    gaps += [days(a, b) for a, b in zip(ts, ts[1:]) if days(a, b) > 0.5]
R["fp_gap_median_days"] = float(np.median(gaps))
R["fp_gap_p90_days"] = float(np.percentile(gaps, 90))
R["fp_gap_mean_days"] = float(np.mean(gaps))
R["fp_intended_gap_days"] = 1 / 0.15
R["fp_checks_per_valid_run"] = float(np.mean([r["fp_n"] for r in run_rows if not r["outage"]]))
# exponential hazard MLE per group: P(changed | gap g) = 1 - exp(-lambda g)
def hazard_mle(pairs):
    if not pairs:
        return float("nan")
    grid = np.logspace(-4, 0.5, 400)
    ll = []
    for lam in grid:
        s = 0.0
        for g, changed in pairs:
            p = 1 - math.exp(-lam * g)
            p = min(max(p, 1e-9), 1 - 1e-9)
            s += math.log(p) if changed else math.log(1 - p)
        ll.append(s)
    return float(grid[int(np.argmax(ll))])


def fp_pairs(filter_fn):
    out = []
    for ch in fp_valid:
        if ch["ts"] < FILTER_RECOMPUTE:
            continue
        did = ch["document_id"]
        if not filter_fn(doc_by_id[did]):
            continue
        t = parse_ts(ch["ts"])
        prev = max((x for x in obs[did] if x < t - dt.timedelta(hours=1)), default=None)
        if prev is None:
            continue
        out.append((days(prev, t), ch["outcome"] == "changed"))
    return out


ctype_of = {d["id"]: next((v["content_type"] for v in reversed(versions)
                           if v["document_id"] == d["id"]), None) for d in docs}
R["hazard_all_per_day"] = hazard_mle(fp_pairs(lambda d: True))
R["hazard_html_per_day"] = hazard_mle(fp_pairs(lambda d: ctype_of[d["id"]] == "text/html"))
R["hazard_pdf_per_day"] = hazard_mle(fp_pairs(lambda d: ctype_of[d["id"]] == "application/pdf"))
R["hazard_html_halflife_days"] = math.log(2) / R["hazard_html_per_day"] if R["hazard_html_per_day"] else float("nan")
R["hazard_pdf_halflife_days"] = math.log(2) / R["hazard_pdf_per_day"] if R["hazard_pdf_per_day"] else float("nan")
R["n_fp_pairs_post"] = len(fp_pairs(lambda d: True))

# ------------------------------------------------------------------ 6. classifications
pairs = json.load(open(os.path.join(HERE, "pairs", "version_pairs.json")))
cls: dict[tuple, dict] = {}
for f in sorted(glob.glob(os.path.join(HERE, "classifications", "*.json"))):
    if os.path.basename(f) == "overrides.json":
        continue
    for r in json.load(open(f)):
        if (r["slug"], int(r["version"])) in cls:
            print("WARNING: duplicate classification for", r["slug"], r["version"], "in", os.path.basename(f))
        cls[(r["slug"], int(r["version"]))] = r
# Hand-verified overrides (e.g. diffs that turned out to be extractor artefacts when checked
# against the raw HTML). Each entry carries its reason; applied on top of the sub-agent labels.
ovp = os.path.join(HERE, "classifications", "overrides.json")
overrides = json.load(open(ovp)) if os.path.exists(ovp) else []
for o in overrides:
    r = cls.get((o["slug"], int(o["version"])))
    if r:
        r["category"] = o["category"]
        for flag in ("score_change", "license_change", "safety_related", "model_scope_change", "correction"):
            r[flag] = False
        r["override_reason"] = o["reason"]
# Entries with "verified": false are conservative reclassifications that could not be checked
# against the raw capture; the report's "the raw HTML still held every footnote" claim counts only
# verified ones.
# Count only overrides that still apply to a pair in the manifest: versions can be purged from the
# database (the 12 Anthropic footnote-artefact versions, incl. the 3 verified overrides, were deleted
# between the 2026-09-22 and 2026-09-29 snapshots after the extractor fix).
_live = {(p["slug"], p["version"]) for p in pairs}
R["n_overrides"] = sum(1 for o in overrides
                       if (o["slug"], int(o["version"])) in _live and o.get("verified", True))
R["n_overrides_unverified"] = sum(1 for o in overrides
                                  if (o["slug"], int(o["version"])) in _live and not o.get("verified", True))
R["n_overrides_purged"] = sum(1 for o in overrides if (o["slug"], int(o["version"])) not in _live)
R["n_classified_purged"] = sum(1 for k in cls if k not in _live)
# Versions the changelog says were written but that are no longer in document_versions (matched on
# document + content hash). Almost all predate the fingerprint recompute, so the "before" side of every
# pre/post comparison is missing pairs; the cause beyond the documented footnote purge is not recorded.
_have = {(v["document_id"], v["content_hash"]) for v in versions}
_gone = [cl for cl in changelog if cl["action"] == "new_version"
         and (cl["document_id"], cl["d"].get("content_hash")) not in _have]
R["n_versions_missing"] = len(_gone)
R["n_versions_missing_pre_filter"] = sum(1 for cl in _gone if cl["ts"] < FILTER_RECOMPUTE)
slug_to_doc = {d["slug"]: d for d in docs}
for p in pairs:
    p["cls"] = cls.get((p["slug"], p["version"]))
    p["era"] = "post" if p["fetched"] >= FILTER_RECOMPUTE else "pre"
# Tracker-side migrations: the canonical URL (or the served content type) changed between
# the two fetches, e.g. the 2026-08-31 move from announcement pages to full PDFs. The diff then
# compares two different captures, not two revisions by the publisher, so these pairs get a
# deterministic category of their own and are excluded from publisher-change statistics.
vt_of = {v["id"]: v["content_type"] for v in versions}
url_updates: dict[int, list] = collections.defaultdict(list)
for cl in changelog:
    if cl["action"] == "field_update" and cl["d"].get("field") == "canonical_url":
        url_updates[cl["document_id"]].append(cl["ts"])
# A move recorded by the monitor inside the interval is also tracker-side: after a 301 the monitor
# stores the redirect target's content as a new version of the old row (Palisade, 2026-09-24).
for cl in changelog:
    if cl["action"] == "status_change" and cl["d"].get("new") == "moved":
        url_updates[cl["document_id"]].append(cl["ts"])
# The 2026-08-31 canonical_url updates were logged 0-5 s AFTER the new version's fetched_at, so shift
# the whole interval by a small tolerance: an update logged just after the previous version belongs to
# the previous pair, not this one (Gemini PDF edits v481/v513 were otherwise counted as migrations).
MIGRATION_TOL_S = 60
for p in pairs:
    did = slug_to_doc[p["slug"]]["id"]
    _a, _b = parse_ts(p["prev_fetched"]), parse_ts(p["fetched"])
    p["migration"] = (vt_of[p["prev_version"]] != vt_of[p["version"]]) or any(
        (parse_ts(t) - _a).total_seconds() > MIGRATION_TOL_S and (parse_ts(t) - _b).total_seconds() <= MIGRATION_TOL_S
        for t in url_updates[did])
    if p["cls"]:
        p["cls"]["raw_category"] = p["cls"]["category"]
        if p["migration"]:
            p["cls"]["category"] = "tracker_migration"
classified = [p for p in pairs if p["cls"]]
R["n_pairs"] = len(pairs)
R["n_migration_pairs"] = sum(1 for p in pairs if p["migration"])
R["share_migration_pairs"] = pct(R["n_migration_pairs"], len(pairs))
R["migration_raw_categories"] = collections.Counter(
    p["cls"]["raw_category"] for p in classified if p["migration"]).most_common()
R["n_pairs_classified"] = len(classified)
R["n_pairs_removed_docs"] = sum(1 for p in pairs if slug_to_doc[p["slug"]]["status"] == "removed")
CATS = ["furniture", "extraction_noise", "metadata_minor", "content_minor", "content_major",
        "replacement", "tracker_migration"]
SUBSTANTIVE = {"content_minor", "content_major", "replacement"}
cat_counts = collections.Counter(p["cls"]["category"] for p in classified)
R["cat_counts"] = [(k, cat_counts.get(k, 0)) for k in CATS]
for k in CATS:
    R[f"share_cat_{k}"] = pct(cat_counts.get(k, 0), len(classified))
R["n_substantive"] = sum(cat_counts.get(k, 0) for k in SUBSTANTIVE)
R["share_substantive"] = pct(R["n_substantive"], len(classified))
R["share_nonchange"] = pct(cat_counts.get("furniture", 0) + cat_counts.get("extraction_noise", 0),
                           len(classified))
# Soft-gone: the body was replaced while the document was still active (HTTP 200, no recorded
# move or death yet). Keyed on status at detection time, not current status, so a page that later
# gets a real redirect (Palisade, 2026-09-23) stays listed with the date it was resolved, and a
# replacement captured after the move (the redirect target's content) is not counted.
status_changes = collections.defaultdict(list)
for cl in changelog:
    if cl["action"] == "status_change" and cl["d"].get("new") in ("moved", "dead", "removed"):
        status_changes[cl["document_id"]].append((cl["ts"], cl["d"]["new"]))
def _status_after(p):
    later = sorted(x for x in status_changes[slug_to_doc[p["slug"]]["id"]] if x[0] > p["fetched"])
    return later[0] if later else None
def _inactive_at(p):
    return any(ts <= p["fetched"] for ts, _ in status_changes[slug_to_doc[p["slug"]]["id"]])
def _ok_after(p):
    # the link check must have seen a plain HTTP 200 (no redirect) after the body was replaced and
    # before any recorded move/death; otherwise the replacement is just the first sight of a redirect
    # (Mistral Small 4, 2026-08-31 -> moved 2026-09-01)
    did = slug_to_doc[p["slug"]]["id"]
    end = (_status_after(p) or ("9999",))[0]
    return any(ch["document_id"] == did and ch["check_type"] == "link" and ch["outcome"] == "ok"
               and p["fetched"] <= ch["ts"] < end for ch in checks)
R["soft_gone"] = [{"slug": p["slug"], "date": p["fetched"][:10], "summary": p["cls"]["summary"],
                   "resolved": (_status_after(p) or (None, None))[0] and _status_after(p)[0][:10],
                   "resolved_as": (_status_after(p) or (None, None))[1]}
                  for p in classified if p["cls"]["category"] == "replacement"
                  and slug_to_doc[p["slug"]]["status"] != "removed" and not _inactive_at(p)
                  and _ok_after(p)]
R["soft_gone_days_min"] = min((int(days(parse_ts(g["date"]), parse_ts(g["resolved"] or R["snapshot_date"])))
                               for g in R["soft_gone"]), default=0)
R["n_soft_gone_resolved"] = sum(1 for g in R["soft_gone"] if g["resolved"])
R["n_soft_gone_open"] = sum(1 for g in R["soft_gone"] if not g["resolved"])
R["n_soft_gone"] = len(R["soft_gone"])
# substantive share among pairs that are not tracker migrations (publisher-side changes only)
pub_pairs = [p for p in classified if not p["migration"]]
R["n_pub_pairs"] = len(pub_pairs)
R["n_pub_substantive"] = sum(1 for p in pub_pairs if p["cls"]["category"] in SUBSTANTIVE)
R["share_pub_substantive"] = pct(R["n_pub_substantive"], len(pub_pairs))
R["share_pub_nonchange"] = pct(sum(1 for p in pub_pairs if p["cls"]["category"] in ("furniture", "extraction_noise")), len(pub_pairs))
R["share_pub_major"] = pct(sum(1 for p in pub_pairs if p["cls"]["category"] == "content_major"), len(pub_pairs))
for era in ("pre", "post"):
    g = [p for p in classified if p["era"] == era and not p["migration"]]
    cc = collections.Counter(p["cls"]["category"] for p in g)
    R[f"n_pairs_{era}"] = len(g)
    R[f"share_nonchange_{era}"] = pct(cc.get("furniture", 0) + cc.get("extraction_noise", 0), len(g))
    R[f"share_substantive_{era}"] = pct(sum(cc.get(k, 0) for k in SUBSTANTIVE), len(g))
    R[f"share_furniture_{era}"] = pct(cc.get("furniture", 0), len(g))


def cat_table(keyfn, labels):
    rows = []
    for lab in labels:
        g = [p for p in classified if keyfn(p) == lab]
        cc = collections.Counter(p["cls"]["category"] for p in g)
        rows.append((lab, len(g), [cc.get(k, 0) for k in CATS]))
    return rows


R["cat_by_content_type"] = cat_table(lambda p: p["content_type"], ["text/html", "application/pdf"])
R["cat_by_doc_type"] = cat_table(lambda p: p["doc_type"],
                                 [k for k, _ in collections.Counter(p["doc_type"] for p in classified).most_common()])
R["cat_by_publisher"] = cat_table(lambda p: p["publisher"],
                                  [k for k, _ in collections.Counter(p["publisher"] for p in classified).most_common()])
flags = ["score_change", "license_change", "safety_related", "model_scope_change", "correction"]
R["flag_counts"] = [(f, sum(1 for p in classified if p["cls"].get(f))) for f in flags]
R["flag_counts_substantive"] = [(f, sum(1 for p in classified if p["cls"].get(f)
                                        and p["cls"]["category"] in SUBSTANTIVE)) for f in flags]
R["growth"] = collections.Counter(p["cls"].get("growth_direction") for p in classified
                                  if p["cls"]["category"] in SUBSTANTIVE).most_common()
R["conf"] = collections.Counter(p["cls"].get("confidence") for p in classified).most_common()
# docs with >=1 substantive change
sub_docs = {p["slug"] for p in classified if p["cls"]["category"] in SUBSTANTIVE}
R["n_docs_substantive"] = len([s for s in sub_docs if slug_to_doc[s]["status"] != "removed"])
R["share_docs_substantive"] = pct(R["n_docs_substantive"], len(tracked))
R["n_docs_major"] = len({p["slug"] for p in classified if p["cls"]["category"] == "content_major"
                         and slug_to_doc[p["slug"]]["status"] != "removed"})
R["share_docs_major"] = pct(R["n_docs_major"], len(tracked))
# how many stored versions are non-changes (detector precision)
R["detector_precision_all"] = R["share_substantive"] + R["share_cat_metadata_minor"]
# agent change_summary agreement: summary present & category
R["n_pairs_with_summary"] = sum(1 for p in classified if p["change_summary"])
# notable changes list
notable = [p for p in classified if p["cls"].get("notable") and p["cls"]["category"] in SUBSTANTIVE]
notable.sort(key=lambda p: ({"content_major": 0, "replacement": 1, "content_minor": 2}[p["cls"]["category"]],
                            -(p["added"] + p["removed"])))
R["notable"] = [{"slug": p["slug"], "publisher": p["publisher"], "title": p["title"],
                 "date": p["fetched"][:10], "category": p["cls"]["category"],
                 "summary": p["cls"]["summary"], "notable": p["cls"]["notable"],
                 "flags": [f for f in flags if p["cls"].get(f)]} for p in notable]
# Kaplan-Meier: time from first_seen to first substantive change; censor at last valid fp obs
km_groups = {}
for label, filt in (("HTML", lambda d: ctype_of[d["id"]] == "text/html"),
                    ("PDF", lambda d: ctype_of[d["id"]] == "application/pdf")):
    data = []
    for d in tracked:
        if not filt(d):
            continue
        ev = sorted(parse_ts(p["fetched"]) for p in classified
                    if p["slug"] == d["slug"] and p["cls"]["category"] in SUBSTANTIVE)
        last_obs = max(obs.get(d["id"], [d["first_seen_ts"]]))
        if ev:
            data.append((days(d["first_seen_ts"], ev[0]), 1))
        else:
            data.append((days(d["first_seen_ts"], last_obs), 0))
    data.sort()
    n = len(data)
    t_grid, s_grid, s = [0.0], [1.0], 1.0
    at_risk = n
    for t, e in data:
        if e:
            s *= (1 - 1 / at_risk)
            t_grid.append(t)
            s_grid.append(s)
        at_risk -= 1
    km_groups[label] = {"t": t_grid, "s": s_grid, "n": n, "events": sum(e for _, e in data),
                        "max_t": max((t for t, _ in data), default=0)}
    R[f"km_{label.lower()}_n"] = n
    R[f"km_{label.lower()}_events"] = km_groups[label]["events"]
    # share changed by 30 days
    s30 = next((s for t, s in zip(reversed(t_grid), reversed(s_grid)) if t <= 30), 1.0)
    R[f"km_{label.lower()}_changed_by_30d"] = 100 * (1 - s30)

# ------------------------------------------------------------------ 7. curation funnel
adds = [cl for cl in changelog if cl["action"] == "add"]
rejects = [cl for cl in changelog if cl["action"] == "reject"]
fields = [cl for cl in changelog if cl["action"] == "field_update"]
R["n_adds"] = len(adds)
R["adds_by_actor"] = collections.Counter(cl["d"].get("actor") for cl in adds).most_common()
R["n_rejects"] = len(rejects)


def reject_class(reason):
    if reason.startswith("cap_exceeded"):
        return "daily cap reached"
    if reason.startswith("fetch_budget"):
        return "fetch budget reached"
    if reason.startswith("tier_2"):
        return "tier-2 publisher (early policy)"
    if "duplicate" in reason:
        return "duplicate"
    if "retrievable" in reason:
        return "unretrievable"
    if "publication_date" in reason:
        return "publication date unknown"
    return "other validation"


R["rejects_by_class"] = collections.Counter(reject_class(cl["d"].get("reason", ""))
                                            for cl in rejects).most_common()
R["n_field_updates"] = len(fields)
R["field_updates_by_field"] = collections.Counter(cl["d"].get("field") for cl in fields).most_common()
R["field_updates_by_actor"] = collections.Counter(cl["d"].get("actor") for cl in fields).most_common()
R["changelog_by_actor"] = collections.Counter(cl["d"].get("actor") for cl in changelog).most_common()
R["changelog_by_action"] = collections.Counter(cl["action"] for cl in changelog).most_common()
R["false_alarm_rate"] = pct(R["n_removed"], R["n_adds"])
R["n_docs_field_updated"] = len({cl["document_id"] for cl in fields})
R["share_docs_field_updated"] = pct(R["n_docs_field_updated"], R["n_docs_ever"])
R["n_docs_annotated"] = sum(1 for v in versions if v["change_summary"])
cand = {}
cp = os.path.join(DATA, "candidates.json")
if os.path.exists(cp):
    cand = json.load(open(cp))
R["n_candidates_open"] = len(cand.get("candidates", []))
R["adds_per_valid_run_median"] = float(np.median([r["adds"] for r in run_rows if not r["agent_failed"]]))
R["adds_per_valid_run_mean"] = float(np.mean([r["adds"] for r in run_rows if not r["agent_failed"]]))

# ------------------------------------------------------------------ figures
def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"))
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=170)
    plt.close(fig)


TYPE_ORDER = [k for k, _ in R["by_doc_type"]]
TYPE_COL = {t: CAT[i] for i, t in enumerate(TYPE_ORDER)}

# F1 corpus growth + publication months
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.3), gridspec_kw={"width_ratios": [1.25, 1]})
day0 = parse_ts(R["first_seen_min"]).date()
dayN = snapshot_ts.date()
grid = [day0 + dt.timedelta(days=i) for i in range((dayN - day0).days + 1)]
bottom = np.zeros(len(grid))
for t in TYPE_ORDER:
    cum = np.array([sum(1 for d in tracked if d["doc_type"] == t and d["first_seen_ts"].date() <= g)
                    for g in grid])
    ax1.fill_between(grid, bottom, bottom + cum, color=TYPE_COL[t], lw=0, label=pretty(t), step="post")
    bottom += cum
ax1.set_ylabel("documents tracked")
ax1.set_ylim(0, bottom.max() * 1.05)
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax1.annotate("supervised\nbackfill", xy=(grid[1], bottom[1] * 0.55), xytext=(grid[7], bottom[1] * 0.25),
             fontsize=6.5, color=INK2, arrowprops={"arrowstyle": "-", "color": INK2, "lw": 0.6})
ax1.legend(loc="upper center", bbox_to_anchor=(1.1, -0.18), ncol=6, handlelength=1, columnspacing=0.8)
ax1.set_title("(a) corpus growth by date first tracked")
months = [m for m, _ in R["pub_month"]]
bottom = np.zeros(len(months))
for t in TYPE_ORDER:
    vals = np.array([sum(1 for d in tracked if d["doc_type"] == t and (d["publication_date"] or "")[:7] == m)
                     for m in months])
    ax2.bar(range(len(months)), vals, bottom=bottom, color=TYPE_COL[t], width=0.72, lw=0)
    bottom += vals
ax2.set_xticks(range(len(months)))
ax2.set_xticklabels([dt.date(int(m[:4]), int(m[5:]), 1).strftime("%b") for m in months])
ax2.set_ylabel("documents")
ax2.set_title("(b) documents by publication month")
save(fig, "fig_corpus")

# F2 run timeline
fig, ax = plt.subplots(figsize=(6.8, 2.1))
dates = [parse_ts(r["ts"]) for r in run_rows]
OUTC = [("ok", PAL["blue"], "reachable"), ("blocked", PAL["orange"], "bot-blocked (403)"),
        ("redirect", PAL["violet"], "permanent redirect"), ("not_found", PAL["red"], "404"),
        ("error", PAL["yellow"], "fetch error")]
bottom = np.zeros(len(run_rows))
for key, col, lab in OUTC:
    vals = np.array([pct(r[key], r["n_link"]) for r in run_rows])
    ax.bar(dates, vals, bottom=bottom, color=col, width=0.8, lw=0, label=lab)
    bottom += vals
for r, d in zip(run_rows, dates):
    if r["outage"]:
        ax.bar([d], [100], color=GREY, width=0.8, lw=0)
    if r["resume_triggered"]:
        ax.plot([d], [104], marker="v", ms=3.5, color=INK, lw=0)
    if r["agent_failed"]:
        ax.plot([d], [110], marker="x", ms=3.5, color=PAL["red"], lw=0, mew=1)
ax.bar([dates[0]], [0], color=GREY, label="monitor outage (all checks failed)")
ax.plot([], [], marker="v", ms=3.5, color=INK, lw=0, label="run started at resume from suspend")
ax.plot([], [], marker="x", ms=3.5, color=PAL["red"], lw=0, mew=1, label="curation agent failed")
ax.set_ylim(0, 116)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_ylabel("% of link checks")
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=4, handlelength=1, columnspacing=1.0)
ax.grid(False)
save(fig, "fig_runs")

# F3 heatmap docs x runs
run_ids = [r["run_id"] for r in run_rows]
run_index = {rid: i for i, rid in enumerate(run_ids)}
order = sorted(tracked, key=lambda d: (d["publisher"], d["id"]))
CODE = {"none": 0, "ok": 1, "blocked": 2, "redirect_permanent": 3, "not_found": 4, "error": 5, "outage": 6}
COLS = ["#ffffff", "#cde2fb", PAL["orange"], PAL["violet"], PAL["red"], PAL["yellow"], GREY]
M = np.zeros((len(order), len(run_ids)), dtype=int)
row_of = {d["id"]: i for i, d in enumerate(order)}
for ch in checks:
    if ch["check_type"] != "link" or ch["run_id"] not in run_index or ch["document_id"] not in row_of:
        continue
    j = run_index[ch["run_id"]]
    M[row_of[ch["document_id"]], j] = CODE["outage"] if ch["run_id"] in outage_runs else CODE.get(ch["outcome"], 5)
HM_H = 2.0
fig, ax = plt.subplots(figsize=(6.8, HM_H))
from matplotlib.colors import ListedColormap  # noqa: E402
ax.imshow(M, aspect="auto", cmap=ListedColormap(COLS), vmin=-0.5, vmax=6.5, interpolation="nearest")
# publisher separators / labels
pubs = [d["publisher"] for d in order]
groups, prev, start = [], None, 0
for i, p in enumerate(pubs + [None]):
    if p != prev:
        if prev is not None:
            groups.append((i - start, (start + i - 1) / 2, prev.replace("_", " ")))
            ax.axhline(i - 0.5, color="white", lw=0.6)
        prev, start = p, i
# label the largest publishers first, skipping any label that would overlap one already placed
# (a 6 pt label needs about 7 pt of vertical space; the plot area is about 70 % of the figure)
min_gap = len(pubs) * (7 / 72) / (0.7 * HM_H)
placed = []
for n, y, lab in sorted(groups, reverse=True):
    if n >= 8 and all(abs(y - y2) >= min_gap for y2, _ in placed):
        placed.append((y, lab))
placed.sort()
ax.set_yticks([y for y, _ in placed])
ax.set_yticklabels([lab for _, lab in placed], fontsize=6)
xt = [i for i, r in enumerate(run_rows) if parse_ts(r["ts"]).weekday() == 0]
ax.set_xticks(xt)
ax.set_xticklabels([parse_ts(run_rows[i]["ts"]).strftime("%d %b") for i in xt], fontsize=6.5)
ax.set_xlabel("daily run")
ax.grid(False)
ax.tick_params(length=0)
handles = [Patch(color=COLS[1], label="reachable"), Patch(color=COLS[2], label="bot-blocked"),
           Patch(color=COLS[3], label="permanent redirect"), Patch(color=COLS[4], label="404"),
           Patch(color=COLS[5], label="fetch error"), Patch(color=COLS[6], label="monitor outage"),
           Patch(facecolor="white", edgecolor=INK2, label="not yet tracked")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=4, handlelength=1.2,
          columnspacing=1.0)
save(fig, "fig_heatmap")

# F4 discovery lag ECDF
fig, ax = plt.subplots(figsize=(3.3, 2.2))
leads = [(k, n) for k, n, _ in R["lag_by_lead"]]
for i, (lead, n) in enumerate(leads[:5]):
    x = np.sort([r["lag_days"] for r in live if r["lead"] == lead])
    ax.step(np.concatenate([[0], x]), np.concatenate([[0], np.arange(1, len(x) + 1) / len(x)]),
            where="post", color=CAT[i], lw=1.6, label=f"{lead.replace('_', ' ')} (n={n})")
x = np.sort(lags)
ax.step(np.concatenate([[0], x]), np.concatenate([[0], np.arange(1, len(x) + 1) / len(x)]), where="post",
        color=INK, lw=1.0, ls="--", label=f"all (n={len(x)})")
ax.set_xlabel("days from publication to first tracked")
ax.set_ylabel("share of documents")
ax.set_xlim(0, min(60, max(lags) + 1))
ax.set_ylim(0, 1.02)
ax.legend(loc="lower right", handlelength=1.4)
save(fig, "fig_lag")

# F5 change classification + KM
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.05), gridspec_kw={"width_ratios": [1.35, 1], "wspace": 0.42})
CAT_COL = {"furniture": GREY, "extraction_noise": "#d9d8d2", "metadata_minor": PAL["yellow"],
           "content_minor": PAL["aqua"], "content_major": PAL["blue"], "replacement": PAL["red"],
           "tracker_migration": PAL["violet"]}
CAT_LAB = {"furniture": "page furniture", "extraction_noise": "extraction noise",
           "metadata_minor": "metadata / typo", "content_minor": "content: minor",
           "content_major": "content: major", "replacement": "replaced / gone",
           "tracker_migration": "tracker URL migration"}
rows = [("all pairs", len(classified), [cat_counts.get(k, 0) for k in CATS])]
rows += [(f"{pretty(k)} pages", n, v) for k, n, v in R["cat_by_content_type"]]
rows += [(pretty(k), n, v) for k, n, v in R["cat_by_doc_type"] if n >= 10]
rows += [("before filter fix, excl. migrations", R["n_pairs_pre"], [sum(1 for p in classified if p["era"] == "pre" and not p["migration"] and p["cls"]["category"] == k) for k in CATS]),
         ("after filter fix, excl. migrations", R["n_pairs_post"], [sum(1 for p in classified if p["era"] == "post" and not p["migration"] and p["cls"]["category"] == k) for k in CATS])]
ylab = [f"{lab} (n={n})" for lab, n, _ in rows]
left = np.zeros(len(rows))
for k_i, k in enumerate(CATS):
    vals = np.array([100 * v[k_i] / n if n else 0 for _, n, v in rows])
    ax1.barh(range(len(rows)), vals, left=left, color=CAT_COL[k], height=0.7, lw=0, label=CAT_LAB[k])
    left += vals
ax1.set_yticks(range(len(rows)))
ax1.set_yticklabels(ylab, fontsize=6.5)
ax1.invert_yaxis()
ax1.set_xlim(0, 100)
ax1.set_xlabel("% of detected version changes")
ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=4, handlelength=1, columnspacing=0.8)
ax1.set_title("(a) what a detected change turned out to be")
for i, (lab, g) in enumerate(km_groups.items()):
    ax2.step(g["t"] + [g["max_t"]], [100 * (1 - s) for s in g["s"]] + [100 * (1 - g["s"][-1])],
             where="post", color=CAT[i], lw=1.6, label=f"{lab}: {g['events']}/{g['n']} changed")
ax2.set_xlabel("days since first tracked")
ax2.set_ylabel("% with a substantive change")
ax2.set_xlim(0, max(g["max_t"] for g in km_groups.values()) + 1)
ax2.set_ylim(0, None)
ax2.legend(loc="lower right", handlelength=1.2, fontsize=6.5, borderaxespad=0.3)
ax2.set_title("(b) first substantive change (Kaplan-Meier)")
save(fig, "fig_changes")

# F6 funnel + reject reasons
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.0), gridspec_kw={"width_ratios": [1, 1], "wspace": 0.95})
stages = [("index links seen", R["n_index_links"]), ("open candidates", R["n_candidates_open"]),
          ("proposals rejected", R["n_rejects"]), ("documents added", R["n_adds"]),
          ("removed by audit", R["n_removed"]), ("tracked now", R["n_tracked"])]
ax1.barh(range(len(stages)), [v for _, v in stages], color=PAL["blue"], height=0.65, lw=0)
for i, (_, v) in enumerate(stages):
    inside = v > R["n_index_links"] * 0.6
    ax1.text(v - R["n_index_links"] * 0.02 if inside else v + R["n_index_links"] * 0.01, i, fmt(v),
             va="center", ha="right" if inside else "left", fontsize=7, color="white" if inside else INK)
ax1.set_yticks(range(len(stages)))
ax1.set_yticklabels([s for s, _ in stages], fontsize=7)
ax1.invert_yaxis()
ax1.set_xlim(0, R["n_index_links"] * 1.18)
ax1.set_title("(a) curation funnel (counts)")
rc = R["rejects_by_class"]
ax2.barh(range(len(rc)), [v for _, v in rc], color=PAL["orange"], height=0.65, lw=0)
for i, (_, v) in enumerate(rc):
    ax2.text(v + 0.6, i, fmt(v), va="center", fontsize=7, color=INK)
ax2.set_yticks(range(len(rc)))
ax2.set_yticklabels([k for k, _ in rc], fontsize=7)
ax2.invert_yaxis()
ax2.set_xlim(0, max(v for _, v in rc) * 1.2)
ax2.set_title("(b) why proposals were rejected")
save(fig, "fig_funnel")

# F7 fingerprint gaps + change share by era (comprehensive report)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 2.0))
ax1.hist(gaps, bins=np.arange(0, max(gaps) + 2, 1), color=PAL["blue"], lw=0)
ax1.axvline(R["fp_intended_gap_days"], color=PAL["red"], lw=1, ls="--", label="intended (1/0.15 runs)")
ax1.axvline(R["fp_gap_median_days"], color=INK, lw=1, label="realized median")
ax1.set_xlabel("days between content re-checks of a document")
ax1.set_ylabel("re-check intervals")
ax1.legend(handlelength=1.4)
ax1.set_title("(a) content re-check cadence")
by_run = [(parse_ts(r["ts"]), pct(r["fp_changed"], r["fp_changed"] + r["fp_unchanged"]))
          for r in run_rows if r["fp_changed"] + r["fp_unchanged"] > 0]
ax2.plot([t for t, _ in by_run], [v for _, v in by_run], marker="o", ms=3, color=PAL["blue"], lw=1)
ax2.axvline(parse_ts(FILTER_RECOMPUTE), color=PAL["red"], lw=1, ls="--", label="furniture filter recompute")
ax2.set_ylabel("% of re-checks flagged changed")
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax2.set_ylim(0, 100)
ax2.legend(handlelength=1.4)
ax2.set_title("(b) change-flag rate per run")
save(fig, "fig_fingerprint")

# ------------------------------------------------------------------ tables (LaTeX fragments)
def write_table(name, header, rows, align=None):
    align = align or "l" + "r" * (len(header) - 1)
    lines = ["\\begin{tabular}{" + align + "}", "\\toprule",
             " & ".join(texesc(h) for h in header) + " \\\\", "\\midrule"]
    for r in rows:
        lines.append(" & ".join(texesc(x) if isinstance(x, str) else fmt(x) for x in r) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    open(os.path.join(TAB, name + ".tex"), "w").write("\n".join(lines) + "\n")


def longtable(name, header, rows, align, caption="", label=""):
    head = ["\\toprule", " & ".join(header) + " \\\\", "\\midrule"]
    lines = ["\\begin{longtable}{" + align + "}"]
    if caption:
        lines.append("\\caption{" + caption + "}" + ("\\label{" + label + "}" if label else "") + " \\\\")
    lines += head + ["\\endfirsthead"] + head + ["\\endhead"]
    for r in rows:
        lines.append(" & ".join(r) + " \\\\")
    lines += ["\\bottomrule", "\\end{longtable}"]
    open(os.path.join(TAB, name + ".tex"), "w").write("\n".join(lines) + "\n")



write_table("doc_types", ["Document type", "Tracked", "Share (\\%)"],
            [(pretty(k), n, pct(n, len(tracked))) for k, n in R["by_doc_type"]])
write_table("publishers", ["Publisher", "Tracked"],
            [(k.replace("_", " "), n) for k, n in R["by_publisher"][:12]])
write_table("cat_counts", ["Category", "Pairs", "Share (\\%)"],
            [(CAT_LAB[k], n, pct(n, len(classified))) for k, n in R["cat_counts"]])
write_table("cat_by_content_type", ["Page type", "Pairs"] + [CAT_LAB[k] for k in CATS],
            [(pretty(k), n, *v) for k, n, v in R["cat_by_content_type"]])
write_table("cat_by_publisher", ["Publisher", "Pairs"] + [CAT_LAB[k] for k in CATS],
            [(k.replace("_", " "), n, *v) for k, n, v in R["cat_by_publisher"] if n >= 4])
write_table("link_outcomes", ["Outcome (valid runs)", "Checks", "Share (\\%)", "Documents ever"],
            [(pretty(k), n, pct(n, len(valid_link)), ever.get(k, 0)) for k, n in R["valid_link_outcomes"]])
longtable("runs_by_day", ["Run", "Links", "Reachable", "Blocked", "Errors", "Content checks", "Changed", "Outage", "Resume (s)", "Agent"],
          [(r["date"] + " " + r["ts"][11:16], str(r["n_link"]), str(r["ok"]), str(r["blocked"]), str(r["error"]), str(r["fp_n"]),
            str(r["fp_changed"]), "yes" if r["outage"] else "", "" if r["sec_since_resume"] is None else str(int(r["sec_since_resume"])),
            ("failed" if r["agent_failed"] else "ok") if r["agent_known"] else "no log") for r in run_rows],
          "@{}l" + "r" * 9 + "@{}",
          caption="Every daily run: link probes and their outcomes, content checks, whether the run was a full outage, "
                  "seconds between the host's last resume from suspend and the run start, and the agent phase.",
          label="tab:runs")
write_table("runs", ["Metric", "Value"], [
    ("Daily runs recorded", R["n_runs"]),
    ("Calendar days spanned", R["calendar_days_span"]),
    ("Days with no run", R["n_missing_days"]),
    ("Runs with every link check failing (monitor outage)", R["n_outage_runs"]),
    ("\\quad of which started within 2 min of resume from suspend", R["n_resume_triggered_outages"]),
    ("Runs with partial fetch errors", R["n_partial_runs"]),
    ("Runs whose curation agent failed", R["n_agent_failed_runs"]),
    ("\\quad of which authentication (OAuth) failures", R["n_agent_auth_failed"]),
    ("Runs where both monitor and agent succeeded", R["n_fully_good_runs"]),
    ("Longest consecutive outage streak (runs)", R["longest_outage_streak"]),
])
write_table("lag_by_lead", ["Lead source", "Documents", "Median lag (days)"],
            [(k.replace("_", " "), n, m) for k, n, m in R["lag_by_lead"]])
write_table("rejects", ["Rejection reason", "Proposals"], R["rejects_by_class"])
write_table("field_updates", ["Field", "Updates"], [(pretty(k), n) for k, n in R["field_updates_by_field"]])
write_table("moved", ["Date", "Document", "Redirect target"],
            [(m["date"], m["slug"], m["to"]) for m in R["moved_events"]], align="lll")
write_table("notable", ["Date", "Publisher", "What changed"],
            [(n["date"], n["publisher"].replace("_", " "), n["summary"]) for n in R["notable"][:12]],
            align="llp{9.2cm}")
# Report table: publisher-side changes that a transparency reader cares about, chosen by rule:
# corrections, license changes, pages that went away, then the largest major changes; by date.
sel = []
for p in classified:
    if p["migration"] or p["cls"]["category"] not in SUBSTANTIVE:
        continue
    if p["cls"]["category"] == "replacement" and (p["slug"], p["fetched"][:10]) not in {
            (g["slug"], g["date"]) for g in R["soft_gone"]}:
        continue  # only soft-gone replacements; recorded moves are counted as such
    txt = (p["cls"]["summary"] + " " + (p["cls"].get("notable") or "")).lower()
    undisclosed = any(k in txt for k in ("silent", "quietly", "no change log", "no changelog",
                                         "no erratum", "without any note", "without a note")) and not any(
        k in p["cls"]["summary"].lower() for k in ("changelog", "change log", "erratum", "correction note"))
    kind = ("undisclosed" if undisclosed and p["cls"]["category"] in ("content_minor", "content_major")
            else "correction" if p["cls"].get("correction")
            else "gone" if p["cls"]["category"] == "replacement"
            else "license" if p["cls"].get("license_change")
            else "major" if p["cls"]["category"] == "content_major" else "")
    if kind:
        sel.append((kind, p))
prio = {"undisclosed": 0, "correction": 1, "gone": 2, "license": 3, "major": 4}
sel.sort(key=lambda kp: (prio[kp[0]], -(kp[1]["added"] + kp[1]["removed"])))
# One row per distinct change: the same correction can propagate to several documents of a
# publisher (same first decimal number in the summary), which is itself worth showing as a count.
seen, groups = {}, []
for kind, p in sel:
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", p["cls"]["summary"])
    key = (p["publisher"], kind, m.group(1) if m else p["slug"])
    if key in seen:
        groups[seen[key]]["n"] += 1
        groups[seen[key]]["members"].append(p)
        continue
    seen[key] = len(groups)
    groups.append({"kind": kind, "p": p, "n": 1, "members": [p]})
rows = []
caps = {"undisclosed": 3, "correction": 2, "gone": 2, "license": 1, "major": 1}
for g in groups:
    if caps[g["kind"]] <= 0:
        continue
    caps[g["kind"]] -= 1
    p = g["p"]
    title = p["title"] if len(p["title"]) <= 38 else p["title"][:36].rstrip() + "..."
    rows.append((p["fetched"][:10], p["publisher"].replace("_", " ") + ": " + title,
                 {"undisclosed": "no change log", "correction": "dated correction",
                  "gone": "moved behind 200", "license": "licence", "major": "major edit"}[g["kind"]],
                 p["cls"]["summary"].replace("~", "approx. ")
                 + (f" (same change in {g['n']} documents)" if g["n"] > 1 else "")))
rows.sort()
R["notable_kinds"] = collections.Counter(r[2] for r in rows).most_common()
main_table_slugs = {g["p"]["slug"] for g in groups}

# Appendix: every substantive publisher-side change with the URL and version ids needed to verify it.
CAT_SHORT = {"content_minor": "minor", "content_major": "major", "replacement": "replaced"}
app_rows = []
sub_pairs = sorted((p for p in classified if not p["migration"] and p["cls"]["category"] in SUBSTANTIVE),
                   key=lambda p: (p["fetched"], p["slug"]))
for i, p in enumerate(sub_pairs, 1):
    fl = ", ".join(f.replace("_change", "").replace("_related", "").replace("model_scope", "scope")
                   for f in flags if p["cls"].get(f))
    app_rows.append((
        f"A{i}", p["fetched"][:10], texesc(p["publisher"].replace("_", " ")),
        texesc(p["title"][:60] + ("..." if len(p["title"]) > 60 else "")) + "\\newline\\url{" + p["url"] + "}",
        CAT_SHORT[p["cls"]["category"]] + (" (" + fl + ")" if fl else "") + f"\\newline v{p['prev_version']}$\\to$v{p['version']}",
        texesc(p["cls"]["summary"].replace("~", "approx. "))))
longtable("appendix_changes", ["Id", "Detected", "Publisher", "Document and canonical URL", "Category (flags), versions",
                               "What changed (classifier summary)"], app_rows, "@{}lp{1.5cm}p{1.4cm}p{5.0cm}p{2.1cm}p{4.8cm}@{}",
          caption="All substantive publisher-side changes with URL and version ids.", label="tab:appendix")
R["n_appendix_rows"] = len(app_rows)
# Appendix ids of the pairs the body text names as examples, so each claim points at its row.
# Keys are the report.tex macro names; a pair missing from the appendix renders as "A?" and warns.
_app_id = {(p["slug"], p["version"]): f"A{i}" for i, p in enumerate(sub_pairs, 1)}
BODY_EXAMPLES = {
    "exAstraAppendix": [("openai-gpt-6-astra-system-card", 620)],
    "exGrokLog": [("xai-grok-4-6-model-card", 357)],
    "exAnthropicLog": [("anthropic-claude-opus-4-6-other-6", 579)],
    "exVoiceChat":[("nvidia-nvidia-nemotronlabs-voicechat-11b-model-card", 317)],
    "exCyberExample": [("openai-gpt-5-6-cyber-other", 482)],
    "exLaunchPartner": [("openai-gpt-rosalind-access-policy", 561)],
    "exDaybreakTiers": [("openai-gpt-5-6-sol-access-policy", 646)],
    "exCyberScope": [("anthropic-claude-opus-access-policy", 671)],
    "exCosmos": [("nvidia-cosmos3-super-model-card", 613), ("nvidia-cosmos3-edge-model-card", 614)],
    "exTrainingSummary": [("inclusion-ai-ling-3-0-tiny-model-card", 634), ("inclusion-ai-ling-2-6-1t-model-card", 659),
                          ("inclusion-ai-ling-2-6-flash-model-card", 660), ("inclusion-ai-ring-2-6-1t-model-card", 661),
                          ("inclusion-ai-ling-3-0-flash-vl-model-card", 662)],
}
example_ids = {}
for name, keys in BODY_EXAMPLES.items():
    ids = [_app_id.get(k, "A?") for k in keys]
    if "A?" in ids:
        print(f"WARNING: body example {name} not in appendix: {keys}", file=sys.stderr)
    example_ids[name] = ", ".join(ids)
_prop = max(groups, key=lambda g: g["n"]) if groups else None
example_ids["exPropagated"] = ", ".join(sorted(
    (_app_id.get((p["slug"], p["version"]), "A?") for p in _prop["members"]),
    key=lambda s: int(s[1:]) if s[1:].isdigit() else 0)) if _prop else "A?"
app_gone = [(f"S{i}", g["date"], texesc(g["slug"]), "\\url{" + slug_to_doc[g["slug"]]["canonical_url"] + "}",
             (f"{g['resolved_as']} {g['resolved']}" if g["resolved"] else "still HTTP 200"))
            for i, g in enumerate(R["soft_gone"], 1)]
app_moved = [(m["date"], texesc(m["slug"]), "\\url{" + m["from"] + "}", "\\url{" + m["to"] + "}") for m in R["moved_events"]]
longtable("appendix_moved", ["Date", "Document", "Old canonical URL", "Redirect target"], app_moved, "@{}lp{3.6cm}p{5.6cm}p{5.6cm}@{}",
          caption="Documents whose canonical URL now permanently redirects.", label="tab:moved")
longtable("appendix_soft_gone", ["Id", "Detected", "Document", "URL that kept returning HTTP 200", "Resolved"], app_gone,
          "@{}llp{4.6cm}p{6.4cm}p{2.2cm}@{}",
          caption="Pages whose body became a redirect stub while the URL kept returning HTTP 200, and when the "
                  "tracker first recorded a real redirect (moved) or a 404 (dead) for them.", label="tab:softgone")
R["notable_propagated_max"] = max(g["n"] for g in groups) if groups else 0
R["report_notable_n"] = len(rows)
write_table("notable_report", ["Date", "Publisher: document", "Kind", "What changed (classifier summary)"],
            rows, align="lp{4.1cm}lp{7.9cm}")
write_table("flags", ["Flag", "Pairs", "Of which substantive"],
            [(f.replace("_", " "), a, b) for (f, a), (_, b) in zip(R["flag_counts"], R["flag_counts_substantive"])])

# ------------------------------------------------------------------ macros
DIGITS = {"0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four", "5": "Five",
          "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"}


def macro_name(key):
    parts = key.split("_")
    name = parts[0] + "".join(p.capitalize() for p in parts[1:])
    name = "".join(DIGITS.get(ch, ch) for ch in name)
    name = re.sub(r"[^A-Za-z]", "", name)
    return name


lines = ["% generated by analyze.py -- do not edit"]
for k, v in R.items():
    if isinstance(v, (int, float, str)) and not isinstance(v, bool):
        lines.append(f"\\newcommand{{\\{macro_name(k)}}}{{{texesc(fmt(v))}}}")
    elif isinstance(v, bool):
        lines.append(f"\\newcommand{{\\{macro_name(k)}}}{{{fmt(v)}}}")
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
for k, v in R.items():
    if isinstance(v, int) and not isinstance(v, bool) and 0 <= v < len(WORDS):
        lines.append(f"\\newcommand{{\\{macro_name(k)}Word}}{{{WORDS[v]}}}")
        lines.append(f"\\newcommand{{\\{macro_name(k)}WordCap}}{{{WORDS[v].capitalize()}}}")
# a few derived convenience macros
lines.append(f"\\newcommand{{\\snapshotDatePretty}}{{{snapshot_ts.strftime('%-d %B %Y')}}}")
lines.append(f"\\newcommand{{\\firstSeenMinPretty}}{{{parse_ts(R['first_seen_min']).strftime('%-d %B %Y')}}}")
_sg_res = sorted(g["resolved"] for g in R["soft_gone"] if g["resolved"])
lines.append(f"\\newcommand{{\\softGoneResolvedPretty}}{{{parse_ts(_sg_res[-1]).strftime('%-d %B') if _sg_res else 'n/a'}}}")
lines.append(f"\\newcommand{{\\lastOutagePretty}}{{{parse_ts(R['last_outage_date']).strftime('%-d %B') if R['last_outage_date'] else 'n/a'}}}")
lines.append(f"\\newcommand{{\\lastRunLogPretty}}{{{parse_ts(R['last_run_log_date']).strftime('%-d %B') if R['last_run_log_date'] else 'n/a'}}}")
lines.append(f"\\newcommand{{\\filterRecomputePretty}}{{{parse_ts(FILTER_RECOMPUTE).strftime('%-d %B')}}}")
for name, ids in example_ids.items():
    lines.append(f"\\newcommand{{\\{name}}}{{{ids}}}")
lines.append(f"\\newcommand{{\\topPublisher}}{{{texesc(R['by_publisher'][0][0].replace('_', ' '))}}}")
lines.append(f"\\newcommand{{\\topPublisherN}}{{{R['by_publisher'][0][1]}}}")
lines.append(f"\\newcommand{{\\topBlockedHost}}{{{texesc(R['blocked_docs_by_host'][0][0]) if R['blocked_docs_by_host'] else 'none'}}}")
lines.append(f"\\newcommand{{\\topBlockedHostDocs}}{{{R['blocked_docs_by_host'][0][1] if R['blocked_docs_by_host'] else 0}}}")
lines.append(f"\\newcommand{{\\topBlockedHostChecks}}{{{R['blocked_by_host'][0][1] if R['blocked_by_host'] else 0}}}")
lines.append(f"\\newcommand{{\\topRejectClass}}{{{texesc(R['rejects_by_class'][0][0])}}}")
lines.append(f"\\newcommand{{\\topRejectN}}{{{R['rejects_by_class'][0][1]}}}")
lines.append(f"\\newcommand{{\\topFieldUpdated}}{{{texesc(pretty(R['field_updates_by_field'][0][0]))}}}")
lines.append(f"\\newcommand{{\\topFieldUpdatedN}}{{{R['field_updates_by_field'][0][1]}}}")
lines.append(f"\\newcommand{{\\nDocTypes}}{{{len(R['by_doc_type'])}}}")
lines.append(f"\\newcommand{{\\shareModelCards}}{{{fmt(pct(dict(R['by_doc_type']).get('model_card', 0), len(tracked)))}}}")
lines.append(f"\\newcommand{{\\shareSystemCards}}{{{fmt(pct(dict(R['by_doc_type']).get('system_card', 0), len(tracked)))}}}")
lines.append(f"\\newcommand{{\\shareIndependentEvals}}{{{fmt(pct(dict(R['by_doc_type']).get('independent_eval', 0), len(tracked)))}}}")
lines.append(f"\\newcommand{{\\nSystemCards}}{{{dict(R['by_doc_type']).get('system_card', 0)}}}")
lines.append(f"\\newcommand{{\\nModelCards}}{{{dict(R['by_doc_type']).get('model_card', 0)}}}")
lines.append(f"\\newcommand{{\\nIndependentEvals}}{{{dict(R['by_doc_type']).get('independent_eval', 0)}}}")
lines.append(f"\\newcommand{{\\nHtmlPairs}}{{{R['cat_by_content_type'][0][1]}}}")
lines.append(f"\\newcommand{{\\nPdfPairs}}{{{R['cat_by_content_type'][1][1]}}}")
html_v = R["cat_by_content_type"][0][2]
pdf_v = R["cat_by_content_type"][1][2]
lines.append(f"\\newcommand{{\\shareHtmlNonchange}}{{{fmt(pct(html_v[0] + html_v[1], R['cat_by_content_type'][0][1]))}}}")
lines.append(f"\\newcommand{{\\sharePdfNonchange}}{{{fmt(pct(pdf_v[0] + pdf_v[1], R['cat_by_content_type'][1][1]))}}}")
lines.append(f"\\newcommand{{\\sharePdfSubstantive}}{{{fmt(pct(pdf_v[3] + pdf_v[4] + pdf_v[5], R['cat_by_content_type'][1][1]))}}}")
lines.append(f"\\newcommand{{\\shareHtmlSubstantive}}{{{fmt(pct(html_v[3] + html_v[4] + html_v[5], R['cat_by_content_type'][0][1]))}}}")
pub_flags = {f: sum(1 for p in classified if not p["migration"] and p["cls"].get(f)) for f in flags}
R["flag_counts_publisher_side"] = list(pub_flags.items())
lines.append(f"\\newcommand{{\\nFlagScore}}{{{pub_flags['score_change']}}}")
lines.append(f"\\newcommand{{\\nFlagLicense}}{{{pub_flags['license_change']}}}")
lines.append(f"\\newcommand{{\\nFlagSafety}}{{{pub_flags['safety_related']}}}")
lines.append(f"\\newcommand{{\\nFlagScope}}{{{pub_flags['model_scope_change']}}}")
lines.append(f"\\newcommand{{\\nFlagCorrection}}{{{pub_flags['correction']}}}")
lines.append(f"\\newcommand{{\\nCatMajor}}{{{cat_counts.get('content_major', 0)}}}")
lines.append(f"\\newcommand{{\\nCatMinor}}{{{cat_counts.get('content_minor', 0)}}}")
lines.append(f"\\newcommand{{\\nCatReplacement}}{{{cat_counts.get('replacement', 0)}}}")
lines.append(f"\\newcommand{{\\nCatFurniture}}{{{cat_counts.get('furniture', 0)}}}")
lines.append(f"\\newcommand{{\\nCatNoise}}{{{cat_counts.get('extraction_noise', 0)}}}")
lines.append(f"\\newcommand{{\\nCatMetadata}}{{{cat_counts.get('metadata_minor', 0)}}}")
lines.append(f"\\newcommand{{\\nLeadSources}}{{{len(R['lead_share'])}}}")
top_lead = R["lead_share"][0] if R["lead_share"] else ("none", 0)
lines.append(f"\\newcommand{{\\topLead}}{{{texesc(top_lead[0].replace('_', ' '))}}}")
lines.append(f"\\newcommand{{\\topLeadShare}}{{{fmt(pct(top_lead[1], sum(n for _, n in R['lead_share'])))}}}")
lines.append(f"\\newcommand{{\\lagPseventyfive}}{{{fmt(R['lag_p75_days'])}}}")
lines.append(f"\\newcommand{{\\lagPninety}}{{{fmt(R['lag_p90_days'])}}}")
lines.append(f"\\newcommand{{\\lagWithinThreeDays}}{{{fmt(R['lag_share_within_3d'])}}}")
lines.append(f"\\newcommand{{\\lagWithinSevenDays}}{{{fmt(R['lag_share_within_7d'])}}}")
lines.append(f"\\newcommand{{\\kmHtmlThirty}}{{{fmt(R['km_html_changed_by_30d'])}}}")
lines.append(f"\\newcommand{{\\kmPdfThirty}}{{{fmt(R['km_pdf_changed_by_30d'])}}}")
lines.append(f"\\newcommand{{\\shareNotFoundDocs}}{{{fmt(pct(R['docs_ever_not_found'], R['n_docs_with_valid_checks']))}}}")
lines.append(f"\\newcommand{{\\shareBlockedDocs}}{{{fmt(pct(R['docs_ever_blocked'], R['n_docs_with_valid_checks']))}}}")
lines.append(f"\\newcommand{{\\shareMovedDocs}}{{{fmt(pct(R['n_moved_events'], R['n_docs_with_valid_checks']))}}}")
lines.append(f"\\newcommand{{\\shareResumeOutages}}{{{fmt(pct(R['n_resume_triggered_outages'], R['n_outage_runs']))}}}")
lines.append(f"\\newcommand{{\\shareFullyGoodRuns}}{{{fmt(pct(R['n_fully_good_runs'], R['n_runs_agent_known']))}}}")
lines.append(f"\\newcommand{{\\shareAgentFailedRuns}}{{{fmt(pct(R['n_agent_failed_runs'], R['n_runs']))}}}")
lines.append(f"\\newcommand{{\\nOutageStreakDays}}{{{R['longest_outage_streak']}}}")
lines.append(f"\\newcommand{{\\nNotable}}{{{len(R['notable'])}}}")
lines.append(f"\\newcommand{{\\trackingWeeks}}{{{fmt(R['tracking_days'] / 7)}}}")
lead_med = {k: m for k, _n, m in R["lag_by_lead"]}
for key, name in (("index_diff", "IndexDiff"), ("phase_a_candidate", "PhaseA"), ("agent_search", "AgentSearch"),
                  ("manual", "Manual"), ("index_page", "IndexPage"), ("citation", "Citation")):
    lines.append(f"\\newcommand{{\\lagLead{name}}}{{{fmt(lead_med[key]) if key in lead_med else 'n/a'}}}")
flags_pre = sum(r["fp_changed"] for r in run_rows if r["ts"] < FILTER_RECOMPUTE)
flags_post = sum(r["fp_changed"] for r in run_rows if r["ts"] >= FILTER_RECOMPUTE)
sub_pre = sum(1 for p in classified if p["era"] == "pre" and not p["migration"] and p["cls"]["category"] in SUBSTANTIVE)
sub_post = sum(1 for p in classified if p["era"] == "post" and not p["migration"] and p["cls"]["category"] in SUBSTANTIVE)
R["flags_pre"], R["flags_post"], R["sub_pre"], R["sub_post"] = flags_pre, flags_post, sub_pre, sub_post
R["precision_pre"], R["precision_post"] = pct(sub_pre, flags_pre), pct(sub_post, flags_post)
for k in ("flags_pre", "flags_post", "sub_pre", "sub_post", "precision_pre", "precision_post"):
    lines.append(f"\\newcommand{{\\{macro_name(k)}}}{{{fmt(R[k])}}}")
worst = max((r for r in run_rows if r["partial"]), key=lambda r: r["error"], default=None)
lines.append(f"\\newcommand{{\\worstPartialDate}}{{{parse_ts(worst['ts']).strftime('%-d %B') if worst else 'n/a'}}}")
lines.append(f"\\newcommand{{\\worstPartialErrors}}{{{worst['error'] if worst else 0}}}")
lines.append(f"\\newcommand{{\\worstPartialN}}{{{worst['n_link'] if worst else 0}}}")
lines.append(f"\\newcommand{{\\firstRunPretty}}{{{parse_ts(run_rows[0]['ts']).strftime('%-d %B')}}}")
conf = dict(R["conf"])
lines.append(f"\\newcommand{{\\nConfHigh}}{{{conf.get('high', 0)}}}")
lines.append(f"\\newcommand{{\\nConfMedium}}{{{conf.get('medium', 0)}}}")
lines.append(f"\\newcommand{{\\nConfLow}}{{{conf.get('low', 0)}}}")
lines.append(f"\\newcommand{{\\nOpenaiDocs}}{{{dict(R['by_publisher']).get('openai', 0)}}}")
lines.append(f"\\newcommand{{\\nOutageRunsWithAdds}}{{{sum(1 for r in run_rows if r['outage'] and r['adds'] > 0)}}}")
lines.append(f"\\newcommand{{\\firstMoveDate}}{{{parse_ts(R['moved_events'][0]['date']).strftime('%-d %B') if R['moved_events'] else 'n/a'}}}")
lines.append(f"\\newcommand{{\\nNotableRows}}{{{len(rows)}}}")
open(os.path.join(OUT, "macros.tex"), "w").write("\n".join(lines) + "\n")

# ------------------------------------------------------------------ results.json + comprehensive report
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=str)
json.dump(km_groups, open(os.path.join(OUT, "km.json"), "w"), indent=1)


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(fmt(x) if not isinstance(x, str) else x for x in r) + " |")
    return "\n".join(out)


md = []
md.append(f"# Comprehensive analysis of the cardtrack database (snapshot {R['snapshot_ts']})\n")
md.append("All numbers below are computed by `analyze.py`; figures are in `out/figures/`.\n")
md.append("## 1. Corpus\n")
md.append(f"- Documents ever added: {R['n_docs_ever']}; tracked now: {R['n_tracked']} "
          f"(active {R['n_active']}, moved {R['n_moved']}, dead {R['n_dead']}); removed by audit: {R['n_removed']}.")
md.append(f"- Publishers: {R['n_publishers']}. Stored versions: {R['n_versions']}. Link/fingerprint checks: {R['n_checks']}. Changelog rows: {R['n_changelog']}. Index links seen: {R['n_index_links']}.")
md.append(f"- Publication dates span {R['pub_date_min']} to {R['pub_date_max']}; tracking since {R['first_seen_min']} ({fmt(R['tracking_days'])} days). Backfilled on day one: {R['n_backfill']}; discovered afterwards: {R['n_post_backfill']}.")
md.append(f"- PDF share: {fmt(R['share_pdf'])}%. With safety evaluations: {fmt(R['share_safety_evals'])}%. Independent: {fmt(R['share_independent'])}%.")
md.append(f"- Documents with more than one stored version: {R['n_docs_multi_version']} ({fmt(R['share_docs_multi_version'])}%), max versions {R['max_versions']}.\n")
md.append(md_table(["doc_type", "n"], R["by_doc_type"]) + "\n")
md.append(md_table(["publisher", "n"], R["by_publisher"]) + "\n")
md.append(md_table(["openness", "n"], [(pretty(k), n) for k, n in R["by_openness"]]) + "\n")
md.append(md_table(["risk domain", "n"], R["risk_domains"]) + "\n")
md.append("![corpus](figures/fig_corpus.png)\n")
md.append("## 2. Runs and tracker reliability\n")
md.append(md_table(["run", "date", "links", "ok", "blocked", "redirect", "404", "error", "fp changed", "fp unchanged", "fp error", "outage", "s since resume", "agent failed", "adds"],
                   [(r["run_id"], r["date"], r["n_link"], r["ok"], r["blocked"], r["redirect"], r["not_found"], r["error"], r["fp_changed"], r["fp_unchanged"], r["fp_error"], r["outage"], r["sec_since_resume"] if r["sec_since_resume"] is None else int(r["sec_since_resume"]), r["agent_failed"], r["adds"]) for r in run_rows]) + "\n")
md.append(f"- Runs: {R['n_runs']} over {R['calendar_days_span']} calendar days ({R['n_missing_days']} days without a run). Monitor outages (all link checks errored): {R['n_outage_runs']} ({fmt(R['share_outage_runs'])}%), of which {R['n_resume_triggered_outages']} started within 2 minutes of the laptop resuming from suspend; {R['n_outages_not_resume']} outages were not resume-triggered. Resume-triggered runs that nevertheless succeeded: {R['n_resume_triggered_valid']}.")
md.append(f"- Median seconds between resume and run start: outage runs {fmt(R['median_sec_since_resume_outage'])}, valid runs {fmt(R['median_sec_since_resume_valid'])}. Longest outage streak: {R['longest_outage_streak']} runs.")
md.append(f"- Agent phase failed in {R['n_agent_failed_runs']} runs ({R['n_agent_auth_failed']} authentication). Git push failed in {R['n_push_failed']} runs. Runs with both phases healthy: {R['n_fully_good_runs']}.")
md.append(f"- Staleness at snapshot: median {fmt(R['staleness_median_days'])} days since a document's last valid link check (max {fmt(R['staleness_max_days'])}); never validly checked: {R['docs_never_validly_checked']}.\n")
md.append("![runs](figures/fig_runs.png)\n\n![heatmap](figures/fig_heatmap.png)\n")
md.append("## 3. Availability (target side, outage runs excluded)\n")
md.append(md_table(["outcome", "checks", "docs ever"], [(k, n, ever.get(k, 0)) for k, n in R["valid_link_outcomes"]]) + "\n")
md.append(f"- Valid link checks: {R['n_valid_link_checks']} over {R['n_docs_with_valid_checks']} documents ({fmt(R['doc_days_observed'])} document-days = {fmt(R['doc_years_observed'])} document-years). Always reachable: {R['docs_always_ok']} ({fmt(R['share_docs_always_ok'])}%).")
md.append(f"- Bot-blocked documents: {R['docs_ever_blocked']}, by host: {R['blocked_docs_by_host']}; first block seen {R['first_blocked_date']}; once a document is blocked, the median share of later checks that are also blocked is {fmt(R['blocked_persistence_median'])}%.")
md.append(f"- Permanent redirects (moved): {R['n_moved_events']} ({fmt(R['moves_per_doc_year'])} per document-year). 404s: {R['docs_ever_not_found']} documents. Marked dead: {R['n_dead']}. Removed by human audit: {R['n_removed_human']}; by agent: {R['n_removed_agent']}.")
md.append(md_table(["date", "slug", "from", "to"], [(m["date"], m["slug"], m["from"], m["to"]) for m in R["moved_events"]]) + "\n")
md.append("## 4. Discovery latency\n")
md.append(f"- Documents published on/after {BACKFILL_END} (live discovery): {R['n_lag_live']}. Median lag {fmt(R['lag_median_days'])} d, mean {fmt(R['lag_mean_days'])} d, p75 {fmt(R['lag_p75_days'])} d, p90 {fmt(R['lag_p90_days'])} d, max {fmt(R['lag_max_days'])} d. Within 1 day: {fmt(R['lag_share_within_1d'])}%, 3 days: {fmt(R['lag_share_within_3d'])}%, 7 days: {fmt(R['lag_share_within_7d'])}%.")
md.append(f"- Catch-up discoveries of older documents after the backfill: {R['n_lag_catchup']} (median age {fmt(R['catchup_median_age_days'])} d).")
md.append(md_table(["lead", "n", "median lag d"], R["lag_by_lead"]) + "\n")
md.append(md_table(["doc_type", "n", "median lag d"], R["lag_by_type"]) + "\n")
md.append(md_table(["lead source (post-backfill adds)", "n"], R["lead_share"]) + "\n")
md.append("![lag](figures/fig_lag.png)\n")
md.append("## 5. Content re-checks and change hazard\n")
md.append(f"- Valid fingerprint re-checks: {R['n_fp_valid']}; flagged changed: {R['n_fp_changed']} ({fmt(R['share_fp_changed'])}%). Before the furniture-filter recompute ({FILTER_RECOMPUTE}): {fmt(R['share_fp_changed_pre_filter'])}% of {R['n_fp_pre_filter']}; after: {fmt(R['share_fp_changed_post_filter'])}% of {R['n_fp_post_filter']}.")
md.append(f"- Re-check cadence: intended every {fmt(R['fp_intended_gap_days'])} runs; realized median gap {fmt(R['fp_gap_median_days'])} d (mean {fmt(R['fp_gap_mean_days'])}, p90 {fmt(R['fp_gap_p90_days'])}); {fmt(R['fp_checks_per_valid_run'])} fingerprint checks per valid run.")
md.append(f"- Exponential change hazard (post-filter re-checks, n={R['n_fp_pairs_post']}): all {fmt(R['hazard_all_per_day'])}/day; HTML {fmt(R['hazard_html_per_day'])}/day (half-life {fmt(R['hazard_html_halflife_days'])} d); PDF {fmt(R['hazard_pdf_per_day'])}/day (half-life {fmt(R['hazard_pdf_halflife_days'])} d). Note: this is the fingerprint-level hazard, which still includes furniture leakage.\n")
md.append("![fingerprint](figures/fig_fingerprint.png)\n")
md.append("## 6. What changed (sub-agent classification of version pairs)\n")
md.append(f"- Tracker-side URL/content-type migrations: {R['n_migration_pairs']} pairs ({fmt(R['share_migration_pairs'])}%), raw classifier labels {R['migration_raw_categories']}. Publisher-side pairs: {R['n_pub_pairs']}, substantive {R['n_pub_substantive']} ({fmt(R['share_pub_substantive'])}%), non-change {fmt(R['share_pub_nonchange'])}%, major {fmt(R['share_pub_major'])}%. Soft-gone pages (200 OK but content replaced by stub/redirect): {R['n_soft_gone']}: {R['soft_gone']}.")
md.append(f"- Version pairs: {R['n_pairs']} (classified {R['n_pairs_classified']}; {R['n_pairs_removed_docs']} belong to documents later removed). Substantive (content minor/major/replacement): {R['n_substantive']} ({fmt(R['share_substantive'])}%). Non-changes (furniture + extraction noise): {fmt(R['share_nonchange'])}%.")
md.append(f"- Before filter fix: non-change {fmt(R['share_nonchange_pre'])}% of {R['n_pairs_pre']}; after: {fmt(R['share_nonchange_post'])}% of {R['n_pairs_post']} (substantive after: {fmt(R['share_substantive_post'])}%).")
md.append(f"- Documents with at least one substantive change: {R['n_docs_substantive']} ({fmt(R['share_docs_substantive'])}% of tracked); with a major change: {R['n_docs_major']} ({fmt(R['share_docs_major'])}%). KM share changed by 30 days: HTML {fmt(R['km_html_changed_by_30d'])}% (n={R['km_html_n']}), PDF {fmt(R['km_pdf_changed_by_30d'])}% (n={R['km_pdf_n']}).")
md.append(f"- Classifier confidence: {R['conf']}. Growth direction of substantive changes: {R['growth']}.")
md.append(md_table(["category", "n"], R["cat_counts"]) + "\n")
md.append(md_table(["content type", "n"] + CATS, [(k, n, *v) for k, n, v in R["cat_by_content_type"]]) + "\n")
md.append(md_table(["doc type", "n"] + CATS, [(k, n, *v) for k, n, v in R["cat_by_doc_type"]]) + "\n")
md.append(md_table(["publisher", "n"] + CATS, [(k, n, *v) for k, n, v in R["cat_by_publisher"]]) + "\n")
md.append(md_table(["flag", "pairs", "substantive"], [(f, a, b) for (f, a), (_, b) in zip(R["flag_counts"], R["flag_counts_substantive"])]) + "\n")
md.append("### Notable changes\n")
for n in R["notable"]:
    md.append(f"- {n['date']} {n['publisher']} [{n['category']}] {n['title']}: {n['summary']} {n['notable']} (flags: {', '.join(n['flags']) or 'none'})")
md.append("\n![changes](figures/fig_changes.png)\n")
md.append("## 7. Curation funnel and metadata churn\n")
md.append(f"- Adds: {R['n_adds']} by actor {R['adds_by_actor']}. Rejects: {R['n_rejects']}. Removed after audit: {R['n_removed']} (false-alarm rate {fmt(R['false_alarm_rate'])}% of adds). Open candidates: {R['n_candidates_open']}.")
md.append(f"- Field updates: {R['n_field_updates']} across {R['n_docs_field_updated']} documents ({fmt(R['share_docs_field_updated'])}%); by actor {R['field_updates_by_actor']}. Changelog rows by actor: {R['changelog_by_actor']}; by action: {R['changelog_by_action']}.")
md.append(f"- Adds per run with a working agent: median {fmt(R['adds_per_valid_run_median'])}, mean {fmt(R['adds_per_valid_run_mean'])}; daily runs contributed {R['adds_daily_runs']} adds in {R['n_runs_with_adds']} runs.")
md.append(md_table(["reject class", "n"], R["rejects_by_class"]) + "\n")
md.append(md_table(["field", "updates"], R["field_updates_by_field"]) + "\n")
md.append("![funnel](figures/fig_funnel.png)\n")
open(os.path.join(OUT, "comprehensive_report.md"), "w").write("\n".join(md) + "\n")
print(json.dumps({k: v for k, v in R.items() if isinstance(v, (int, float, str))}, indent=1, default=str)[:6000])
print("figures:", sorted(os.listdir(FIG)))
