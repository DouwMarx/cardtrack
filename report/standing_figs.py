#!/usr/bin/env python3
"""Figures for the standing report that analyze.py does not draw.

Reads out/results.json (appendix_rows = every substantive publisher-side change) and writes
  out/figures/fig_timeline.png     substantive changes per detection week, safety-flagged vs other
  out/figures/fig_corrections.png  every numeric correction read from the diffs: before -> after
  out/figures/fig_edits_by_doc.png documents with the most substantive edits
Palette and conventions follow analyze.py. Run after `run.sh analyze`.
"""
import collections
import datetime as dt
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIG = os.path.join(OUT, "figures")
PAL = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
       "magenta": "#e87ba4", "green": "#008300", "violet": "#4a3aa7", "red": "#e34948"}
GREY = "#b8b7b1"
INK = "#0b0b0b"
INK2 = "#52514e"
plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e5e1", "grid.linewidth": 0.5, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 150, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "font.family": "sans-serif",
})

R = json.load(open(os.path.join(OUT, "results.json")))
rows = R["appendix_rows"]
runs = R["runs"]


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".png"), dpi=170)
    plt.close(fig)


def monday(s):
    d = dt.date.fromisoformat(s[:10])
    return d - dt.timedelta(days=d.weekday())


# ---- F1 timeline: substantive changes per detection week ------------------------------------
weeks = sorted({monday(r["detected"]) for r in rows} | {monday(r["ts"]) for r in runs})
cnt = {w: collections.Counter() for w in weeks}
for r in rows:
    w = monday(r["detected"])
    cnt[w]["safety" if "safety_related" in r["flags"] else "other"] += 1
    if "correction" in r["flags"]:
        cnt[w]["corr"] += 1
valid_runs = collections.Counter(monday(r["ts"]) for r in runs if not r["outage"])
out_runs = collections.Counter(monday(r["ts"]) for r in runs if r["outage"])

fig, ax = plt.subplots(figsize=(6.8, 2.4))
x = range(len(weeks))
saf = [cnt[w]["safety"] for w in weeks]
oth = [cnt[w]["other"] for w in weeks]
ax.bar(x, oth, color=GREY, width=0.72, lw=0, label="other substantive change")
ax.bar(x, saf, bottom=oth, color=PAL["blue"], width=0.72, lw=0, label="classifier safety flag")
for i, w in enumerate(weeks):
    if cnt[w]["corr"]:
        ax.text(i, oth[i] + saf[i] + 0.3, f"{cnt[w]['corr']}", ha="center", va="bottom", fontsize=6.5,
                color=PAL["orange"])
    if out_runs.get(w):
        ax.text(i, -2.4, f"{out_runs[w]}", ha="center", va="center", fontsize=6.5, color=INK2)
ax.text(-0.9, -2.4, "outage runs:", ha="right", va="center", fontsize=6.5, color=INK2)
ax.set_ylim(-3.2, max(o + s for o, s in zip(oth, saf)) + 2.5)
ax.set_yticks(range(0, max(o + s for o, s in zip(oth, saf)) + 3, 3))
ax.set_xticks(list(x))
ax.set_xticklabels([w.strftime("%d %b") for w in weeks], rotation=0, fontsize=6.5)
ax.set_xlabel("detection week (Monday)")
ax.set_ylabel("substantive edits detected")
ax.plot([], [], marker="$1$", ls="", color=PAL["orange"], label="of which corrections (count above bar)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3, handlelength=1, columnspacing=1.2)
ax.grid(axis="x", visible=False)
save(fig, "fig_timeline")

# ---- F2 corrections: numbers changed after publication, verified in the diffs -----------------
# (appendix id, document, metric, before, after, disclosed by a dated note in the document)
CORR = [
    ("A4, A11, A14, A19, A22", "OpenAI GPT-5.5 cards (5)", "hard-negative protein binding, pass@4 (%)", 0.4, 1.48, True),
    ("A50", "OpenAI GPT-6 Astra card", "HealthBench Professional, length-adjusted", 63.4, 64.7, True),
    ("A91, A99", "SecureBio / OpenAI Astra card", "World-Class Biology, GPT-6 Astra (%)", 61.6, 59.2, True),
    ("A84", "Meta Muse Wonder card", "ExploitGym flags (table value)", 92, 20, True),
    ("A12", "xAI Grok 4.6 card", "HackerBench dual-use compliance (%)", 7.8, 6.9, True),
    ("A81", "Epoch AI CVE post", "pre-Mythos monthly CVE record", 440, 490, True),
    ("A42", "Anthropic incident assessment", "PyPI removal window (minutes)", 90, 60, True),
    ("A71", "Mistral Large 4 announcement", "active parameters (B)", 49, 52, False),
    ("A2", "inclusionAI Ling-3.0-tiny card", "activated parameters (B), 19 Aug", 1.3, 1.4, False),
    ("A18", "inclusionAI Ling-3.0-tiny card", "activated parameters (B), 25 Aug", 1.4, 1.3, False),
    ("A56", "inclusionAI Ling-3.0-flash-VL card", "context window (K tokens)", 1000, 256, False),
    ("A6", "NVIDIA VoiceChat 11B card", "tool-calling argument accuracy (%)", 44.2, 42.2, False),
    ("A117", "Thinking Machines Inkling 2 Small card", "Tax Agent Bench, Inkling 2 Small (%)", 65.8, 38.9, False),
]
CORR.sort(key=lambda t: abs(100 * (t[4] - t[3]) / t[3]), reverse=True)
fig, ax = plt.subplots(figsize=(6.8, 3.0))
y = range(len(CORR))
for i, (aid, doc, metric, b, a, disc) in enumerate(CORR):
    rel = 100 * (a - b) / b
    col = PAL["blue"] if disc else PAL["orange"]
    ax.barh(i, rel, color=col, height=0.62, lw=0)
    lab = f"{b:g} → {a:g}"
    ax.text(max(rel, 0) + 4, i, lab, va="center", ha="left", fontsize=6.5, color=INK)
ax.set_yticks(list(y))
ax.set_yticklabels([f"{doc}: {metric}  [{aid}]" for aid, doc, metric, b, a, disc in CORR], fontsize=6.5)
ax.invert_yaxis()
ax.axvline(0, color=INK2, lw=0.6)
ax.set_xlabel("change in the published number (%)")
ax.set_xlim(-110, 330)
ax.legend(handles=[Patch(color=PAL["blue"], label="note or change log in the document"),
                   Patch(color=PAL["orange"], label="no note in the document")],
          loc="lower right", handlelength=1.2)
ax.grid(axis="y", visible=False)
save(fig, "fig_corrections")

# ---- F3 most-edited documents --------------------------------------------------------------
TYPE_COL = {"model_card": PAL["blue"], "independent_eval": PAL["orange"], "other": PAL["aqua"],
            "access_policy": PAL["yellow"], "system_card": PAL["magenta"], "addendum": PAL["green"]}
by_doc = collections.defaultdict(list)
for r in rows:
    by_doc[r["slug"]].append(r)
top = sorted(by_doc.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
fig, ax = plt.subplots(figsize=(6.8, 2.4))
for i, (slug, lst) in enumerate(top):
    saf = sum(1 for r in lst if "safety_related" in r["flags"])
    ax.barh(i, len(lst), color=TYPE_COL[lst[0]["doc_type"]], height=0.62, lw=0)
    ax.barh(i, saf, color="none", edgecolor=INK, hatch="////", height=0.62, lw=0.5)
    ax.text(len(lst) + 0.1, i, f"{len(lst)} ({saf} safety-flagged)", va="center", fontsize=6.5, color=INK)
labels = []
for slug, lst in top:
    t = lst[0]["title"]
    labels.append((lst[0]["publisher"].replace("_", " ") + ": " + (t if len(t) <= 56 else t[:54].rstrip() + "…")))
ax.set_yticks(range(len(top)))
ax.set_yticklabels(labels, fontsize=6.5)
ax.invert_yaxis()
ax.set_xlim(0, max(len(l) for _, l in top) + 2.2)
ax.set_xticks(range(0, max(len(l) for _, l in top) + 1))
LAST = max(r["detected"] for r in rows)
ax.set_xlabel(f"substantive edits detected, 11 Aug to {dt.date.fromisoformat(LAST[:10]).strftime('%d %b %Y')}")
ax.legend(handles=[Patch(color=TYPE_COL[k], label=k.replace("_", " ")) for k in TYPE_COL
                   if any(l[0]["doc_type"] == k for _, l in top)]
          + [Patch(facecolor="none", edgecolor=INK, hatch="////", label="safety-flagged")],
          loc="lower right", handlelength=1.2, ncol=2)
ax.grid(axis="y", visible=False)
save(fig, "fig_edits_by_doc")

# ---- F4 access-policy edits over time ------------------------------------------------------
# Every substantive edit to a document of type access_policy, one row per page, marker per detection.
PUB_COL = {"anthropic": PAL["blue"], "openai": PAL["orange"], "google_deepmind": PAL["aqua"]}
ap = [r for r in rows if r["doc_type"] == "access_policy"]
pages = collections.defaultdict(list)
for r in ap:
    pages[r["slug"]].append(r)
page_order = sorted(pages, key=lambda s: (pages[s][0]["publisher"], min(r["detected"] for r in pages[s])))
d0 = min(dt.date.fromisoformat(r["ts"][:10]) for r in runs)
d1 = max(dt.date.fromisoformat(r["ts"][:10]) for r in runs)
fig, ax = plt.subplots(figsize=(6.8, 2.9))
for i, slug in enumerate(page_order):
    lst = pages[slug]
    col = PUB_COL.get(lst[0]["publisher"], GREY)
    ax.hlines(i, d0, d1, color="#e6e5e1", lw=0.8, zorder=1)
    for r in lst:
        x = dt.date.fromisoformat(r["detected"][:10])
        big = r["category"] == "content_major"
        ax.scatter([x], [i], s=46 if big else 18, color=col, marker="o" if big else "o",
                   edgecolor=INK if "model_scope_change" in r["flags"] else "none", linewidths=0.9, zorder=3)
labels = []
for slug in page_order:
    t = pages[slug][0]["title"]
    labels.append(pages[slug][0]["publisher"].replace("_", " ") + ": " + (t if len(t) <= 44 else t[:42].rstrip() + "…"))
ax.set_yticks(range(len(page_order)))
ax.set_yticklabels(labels, fontsize=6.5)
ax.invert_yaxis()
ax.set_xlim(d0, d1 + dt.timedelta(days=1))
import matplotlib.dates as mdates  # noqa: E402
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.set_xlabel("detection date, 2026")
ax.grid(axis="y", visible=False)
from matplotlib.lines import Line2D  # noqa: E402
ax.legend(handles=[Line2D([], [], ls="", marker="o", ms=7, color=GREY, label="major edit"),
                   Line2D([], [], ls="", marker="o", ms=4.5, color=GREY, label="minor edit"),
                   Line2D([], [], ls="", marker="o", ms=7, color="none", markeredgecolor=INK, label="model coverage changed")],
          loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, handlelength=1.2)
save(fig, "fig_access_timeline")

json.dump({"corrections": [dict(ids=a, document=d, metric=m, before=b, after=af, disclosed=di,
                                rel_change_pct=round(100 * (af - b) / b, 1)) for a, d, m, b, af, di in CORR],
           "weekly": {w.isoformat(): dict(cnt[w]) | {"valid_runs": valid_runs.get(w, 0), "outage_runs": out_runs.get(w, 0)}
                      for w in weeks},
           "most_edited": [(slug, len(lst), sum(1 for r in lst if "safety_related" in r["flags"])) for slug, lst in top],
           "access_policy_edits": {slug: [(r["id"], r["detected"], r["category"], r["flags"]) for r in pages[slug]] for slug in page_order}},
          open(os.path.join(OUT, "standing_figs.json"), "w"), indent=1)
print("wrote fig_timeline, fig_corrections, fig_edits_by_doc")
