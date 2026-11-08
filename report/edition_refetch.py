#!/usr/bin/env python3
"""Content re-fetch outcomes per week for the two hosts that refuse the tracker (2026-11-08 edition).

Writes out/figures/fig_refetch.png and out/refetch.json. Every value comes from link_checks
(check_type='fingerprint', i.e. the content re-fetches that can detect an edit), grouped by the
Monday of the check date. Outage runs (every link check errored) are excluded by the same rule
analyze.py uses, via out/results.json.
"""
import collections
import datetime as dt
import json
import os
import re
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

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
outage_runs = {r["run_id"] for r in R["runs"] if r["outage"]}
c = sqlite3.connect("file:" + os.path.join(HERE, "data", "docs.sqlite.snapshot") + "?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: [dict(r) for r in c.execute(s, a)]  # noqa: E731
host = lambda u: re.sub(r"^https?://([^/]+).*$", r"\1", u)  # noqa: E731
LAST = json.load(open(os.path.join(OUT, "edition.json")))["last_edition_snapshot"]

rows = q("SELECT l.ts, l.run_id, l.http_status s, d.canonical_url u FROM link_checks l JOIN documents d ON d.id=l.document_id "
         "WHERE l.check_type='fingerprint' ORDER BY l.ts")
rows = [r for r in rows if r["run_id"] not in outage_runs]
HOSTS = {"huggingface.co": ("huggingface.co", {"200": PAL["blue"], "429": PAL["orange"]}, "HTTP 429 (rate limited)"),
         "openai.com": ("openai.com + help.openai.com", {"200": PAL["blue"], "403": PAL["red"]}, "HTTP 403 (blocked)")}
norm_host = lambda h: "openai.com" if h in ("openai.com", "help.openai.com") else h  # noqa: E731
wk = {h: collections.defaultdict(collections.Counter) for h in HOSTS}
for r in rows:
    h = norm_host(host(r["u"]))
    if h not in HOSTS:
        continue
    d = dt.date.fromisoformat(r["ts"][:10])
    wk[h][d - dt.timedelta(days=d.weekday())][str(r["s"])] += 1
weeks = sorted(set().union(*[set(w) for w in wk.values()]))
weeks = [w for w in weeks if w >= dt.date(2026, 8, 31)]   # after the furniture-filter recompute, when re-checks became routine

J = {"weeks": [w.isoformat() for w in weeks]}
fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.7), sharex=True)
for ax, (h, (label, col, refused_label)) in zip(axes, HOSTS.items()):
    ok = np.array([wk[h][w]["200"] for w in weeks])
    other_code = [k for k in col if k != "200"][0]
    bad = np.array([wk[h][w][other_code] for w in weeks])
    rest = np.array([sum(wk[h][w].values()) - wk[h][w]["200"] - wk[h][w][other_code] for w in weeks])
    ax.bar(range(len(weeks)), ok, color=col["200"], width=0.72, lw=0, label="HTTP 200 (content compared)")
    ax.bar(range(len(weeks)), bad, bottom=ok, color=col[other_code], width=0.72, lw=0, label=refused_label)
    if rest.any():
        ax.bar(range(len(weeks)), rest, bottom=ok + bad, color=GREY, width=0.72, lw=0, label="other")
    tot = ok + bad + rest
    for i, (o, t) in enumerate(zip(ok, tot)):
        if t:
            ax.text(i, t + 0.8, f"{100 * o / t:.0f}%", ha="center", fontsize=5.8, color=INK2)
    ax.set_xticks(range(len(weeks)))
    ax.set_xticklabels([w.strftime("%d %b") for w in weeks], fontsize=6, rotation=45, ha="right")
    ax.set_title(f"{label}", loc="left")
    ax.set_ylim(0, tot.max() * 1.12)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), handlelength=1, fontsize=6.5, ncol=1)
    J[h] = {w.isoformat(): dict(wk[h][w]) for w in weeks}
    J[h + "_window"] = dict(sum((wk[h][w] for w in weeks if w >= dt.date.fromisoformat(LAST[:10]) - dt.timedelta(days=dt.date.fromisoformat(LAST[:10]).weekday())), collections.Counter()))
axes[0].set_ylabel("content re-fetches per week\n(label: share answered HTTP 200)")
fig.supxlabel("week of the daily run (Monday)", y=-0.1, fontsize=8)
fig.savefig(os.path.join(OUT, "figures", "fig_refetch.png"), dpi=170)
plt.close(fig)

# window totals by exact window (checks after the last edition's snapshot)
win = [r for r in rows if r["ts"] > LAST]
J["window"] = {h: dict(collections.Counter(str(r["s"]) for r in win if norm_host(host(r["u"])) == h)) for h in HOSTS}
J["window_all"] = dict(collections.Counter(str(r["s"]) for r in win))
J["hf_429_first"] = min(r["ts"] for r in rows if r["s"] == 429)[:10]
J["hf_429_docs"] = len({r["u"] for r in rows if r["s"] == 429})
J["hf_docs_tracked"] = len(q("SELECT id FROM documents WHERE status='active' AND canonical_url LIKE 'https://huggingface.co/%'"))
J["openai_403_window_docs"] = len({r["u"] for r in win if r["s"] == 403})
json.dump(J, open(os.path.join(OUT, "refetch.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in J.items() if k not in HOSTS}, indent=1))
