#!/usr/bin/env python3
"""Corrections ledger for the weekly briefing (run after analyze.py and edition.py).

Every substantive publisher-side change whose classifier record carries the `correction`
flag, with the disclosure class edition.py assigned to it (dated note / called silent /
neither). Writes out/corrections.json, out/tables/edition_corrections.md and
out/figures/fig_corrections.png. Everything derives from out/results.json and out/edition.json.
"""
import collections
import datetime as dt
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(OUT, "results.json")))
E = json.load(open(os.path.join(OUT, "edition.json")))
dated = set(E["disclosure_dated_ids"])
silent = set(E["disclosure_silent_ids"])

rows = [a for a in R["appendix_rows"] if "correction" in a["flags"]]
for a in rows:
    a["disclosure"] = "dated note" if a["id"] in dated else ("called silent" if a["id"] in silent else "neither")
    a["score"] = "score_change" in a["flags"]
    a["safety"] = "safety_related" in a["flags"]

C = {
    "n": len(rows),
    "n_docs": len({a["slug"] for a in rows}),
    "n_score": sum(a["score"] for a in rows),
    "n_safety": sum(a["safety"] for a in rows),
    "by_disclosure": dict(collections.Counter(a["disclosure"] for a in rows)),
    "score_by_disclosure": dict(collections.Counter(a["disclosure"] for a in rows if a["score"])),
    "text_by_disclosure": dict(collections.Counter(a["disclosure"] for a in rows if not a["score"])),
    "by_publisher": {},
    "by_doc_type": dict(collections.Counter(a["doc_type"] for a in rows)),
    "ids": [a["id"] for a in rows],
    "share_of_substantive": len(rows) / len(R["appendix_rows"]),
    "n_substantive": len(R["appendix_rows"]),
}
pubs = collections.OrderedDict()
for a in rows:
    p = pubs.setdefault(a["publisher"], collections.Counter())
    p["n"] += 1
    p["score"] += a["score"]
    p[a["disclosure"]] += 1
order = sorted(pubs, key=lambda k: (-pubs[k]["n"], k))
C["by_publisher"] = {k: dict(pubs[k]) for k in order}

# table: per publisher
lines = ["| Publisher | Corrections | Of which a score | Dated note | Called silent | Neither |", "|---|---|---|---|---|---|"]
for k in order:
    p = pubs[k]
    lines.append(f"| {k.replace('_', ' ')} | {p['n']} | {p['score']} | {p['dated note']} | {p['called silent']} | {p['neither']} |")
lines.append(f"| all publishers | {C['n']} | {C['n_score']} | {C['by_disclosure'].get('dated note', 0)} | "
             f"{C['by_disclosure'].get('called silent', 0)} | {C['by_disclosure'].get('neither', 0)} |")
open(os.path.join(OUT, "tables", "edition_corrections.md"), "w").write("\n".join(lines) + "\n")

# table: every correction, for the appendix-style listing
lines = ["| Id | Detected | Publisher | Document | Versions | Score changed | Disclosure (rule) | What was corrected (classifier summary) |",
         "|---|---|---|---|---|---|---|---|"]
for a in sorted(rows, key=lambda a: a["detected"]):
    lines.append(f"| {a['id']} | {a['detected']} | {a['publisher'].replace('_', ' ')} | "
                 f"[{a['title'][:45] + ('...' if len(a['title']) > 45 else '')}](https://systemcards.org/docs/{a['slug']}.html) | "
                 f"v{a['prev_version']}→v{a['version']} | {'yes' if a['score'] else 'no'} | {a['disclosure']} | {a['summary'].replace('|', chr(92) + '|')} |")
open(os.path.join(OUT, "tables", "edition_corrections_all.md"), "w").write("\n".join(lines) + "\n")

# figure: one dot per correction, publisher rows, detection date on x, colour = disclosure class
COL = {"dated note": PAL["blue"], "called silent": PAL["orange"], "neither": GREY}
LAB = {"dated note": "summary mentions a dated note or change log",
       "called silent": "classifier called the edit silent or undisclosed",
       "neither": "neither (unknown)"}
fig, ax = plt.subplots(figsize=(6.8, 2.6))
ypos = {k: i for i, k in enumerate(order)}
# spread same-day same-publisher dots a little so they do not hide each other
seen = collections.Counter()
for a in sorted(rows, key=lambda a: a["detected"]):
    d = dt.date.fromisoformat(a["detected"])
    key = (a["publisher"], a["detected"])
    off = (seen[key] - 0) * 0.18
    seen[key] += 1
    if a["disclosure"] == "neither":
        ax.scatter(d, ypos[a["publisher"]] + off, s=46, facecolor="white", edgecolor=INK2, lw=1.0, zorder=3)
    else:
        ax.scatter(d, ypos[a["publisher"]] + off, s=46, color=COL[a["disclosure"]], lw=0, zorder=3)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([f"{k.replace('_', ' ')} ({pubs[k]['n']})" for k in order], fontsize=6.5)
ax.invert_yaxis()
ax.set_xlabel("detection date (lags the edit by up to one re-check interval)")
ax.set_ylabel("")
ax.grid(axis="x")
ax.grid(axis="y", lw=0.3)
handles = [Line2D([], [], marker="o", ls="", color=COL[k], label=LAB[k], markersize=6) for k in ("dated note", "called silent")]
handles.append(Line2D([], [], marker="o", ls="", markerfacecolor="white", markeredgecolor=INK2, label=LAB["neither"], markersize=6))
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3, handlelength=1, columnspacing=1.2)
import matplotlib.dates as mdates  # noqa: E402
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=15))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d %b"))
ax.tick_params(axis="x", which="minor", labelsize=7)
ax.set_xlim(dt.date(2026, 8, 10), dt.date(2026, 11, 3))
fig.savefig(os.path.join(OUT, "figures", "fig_corrections.png"), dpi=170)
plt.close(fig)

json.dump(C, open(os.path.join(OUT, "corrections.json"), "w"), indent=1)
print(json.dumps(C, indent=1))
