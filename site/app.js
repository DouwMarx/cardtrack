/* cardtrack table UI: filter, facets, sort, column toggles, CSV export.
   Loads ./data/metadata.json; no framework, no external requests. */
"use strict";

const COLUMNS = [
  { key: "title", label: "Title", show: true },
  { key: "publisher", label: "Publisher", show: true },
  { key: "doc_type", label: "Type", show: true },
  { key: "model_names", label: "Models", show: true },
  { key: "publication_date", label: "Published", show: true },
  { key: "safety_evals", label: "Safety evals", show: true },
  { key: "risk_domains", label: "Risk domains", show: false },
  { key: "openness", label: "Openness", show: true },
  { key: "canonical_url", label: "Source", show: true },
  { key: "status", label: "Status", show: false },
  { key: "version_count", label: "Versions", show: false },
  { key: "first_seen", label: "First seen", show: false },
];

const OPENNESS_LABELS = {
  restricted: "restricted access",
  closed: "closed",
  open_weight_restrictive: "open (restrictive)",
  open_weight_permissive: "open (permissive)",
  na: "n/a",
};

const state = {
  docs: [],
  publishers: {},
  riskLabels: {},   // key -> display, from metadata.json (config-defined vocabulary)
  q: "",
  facets: { publisher: new Set(), doc_type: new Set(), openness: new Set(),
            risk: new Set(), is_independent: "", safety: "" },
  sort: { key: "publication_date", dir: -1 },
  visible: new Set(COLUMNS.filter(c => c.show).map(c => c.key)),
};

const msels = {}; // populated in main() once options are known
let loaded = false; // render() is inert until metadata.json arrives

const $ = id => document.getElementById(id);

function norm(s) { return (s || "").toString().toLowerCase(); }

function matches(d) {
  const q = norm(state.q);
  if (q) {
    // metadata scope only: identity fields plus the date (so "2026" works), not bodies
    const hay = norm(d.title) + " " + norm((d.model_names || []).join(" ")) + " " +
                norm(d.publisher) + " " + norm(d.publication_date);
    if (!q.split(/\s+/).every(tok => hay.includes(tok))) return false;
  }
  const f = state.facets;
  if (f.publisher.size && !f.publisher.has(d.publisher)) return false;
  if (f.doc_type.size && !f.doc_type.has(d.doc_type)) return false;
  if (f.is_independent !== "" && String(d.is_independent) !== f.is_independent) return false;
  if (f.safety !== "" && String(d.safety_evals) !== f.safety) return false;
  if (f.openness.size && !f.openness.has(d.openness || "na")) return false;
  // array-valued facet: any selected tag present on the doc matches
  if (f.risk.size && !(d.risk_domains || []).some(r => f.risk.has(r))) return false;
  return true;
}

function cmp(a, b, key) {
  let va = a[key], vb = b[key];
  if (Array.isArray(va)) va = va.join(", ");
  if (Array.isArray(vb)) vb = vb.join(", ");
  if (typeof va === "number" && typeof vb === "number") return va - vb;
  return String(va).localeCompare(String(vb));
}

function filtered() {
  const rows = state.docs.filter(matches);
  rows.sort((a, b) => {
    // unknown values sort last regardless of direction
    const va = a[state.sort.key], vb = b[state.sort.key];
    const aNull = va == null || va === "", bNull = vb == null || vb === "";
    if (aNull && bNull) return 0;
    if (aNull) return 1;
    if (bNull) return -1;
    return state.sort.dir * cmp(a, b, state.sort.key);
  });
  return rows;
}

function cellHtml(d, key) {
  const esc = s => String(s).replace(/[&<>"']/g,
    c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  switch (key) {
    case "title":
      return `<td class="title"><a href="./docs/${esc(d.slug)}.html">${esc(d.title)}</a></td>`;
    case "model_names":
      return `<td class="models">${esc((d.model_names || []).join(", "))}</td>`;
    case "risk_domains": {
      const tags = d.risk_domains || [];
      if (!tags.length) return "<td></td>";
      return `<td>${tags.map(r =>
        `<span class="badge risk-domain">${esc(state.riskLabels[r] || r)}</span>`).join(" ")}</td>`;
    }
    case "status":
      return `<td><span class="badge status-${esc(d.status)}">${esc(d.status)}</span></td>`;
    case "safety_evals": {
      if (d.safety_evals === 1) return '<td><span class="badge safety-yes">yes</span></td>';
      if (d.safety_evals === 0) return '<td><span class="badge safety-no">none</span></td>';
      return '<td><span class="badge">?</span></td>';
    }
    case "publisher": {
      const badge = d.is_independent ? ' <span class="badge independent">indep.</span>' : "";
      const home = (state.publishers[d.publisher] || {}).homepage || "";
      const name = /^https?:\/\//i.test(home)
        ? `<a href="${esc(home)}" rel="noopener nofollow">${esc(d.publisher)}</a>`
        : esc(d.publisher);
      return `<td>${name}${badge}</td>`;
    }
    case "openness": {
      const label = OPENNESS_LABELS[d.openness];
      if (!label || d.openness == null) return '<td><span class="badge">n/a</span></td>';
      const cls = { closed: "openness-closed", open_weight_restrictive: "openness-restrictive",
                    open_weight_permissive: "openness-permissive" }[d.openness] || "";
      return `<td><span class="badge ${cls}">${label}</span></td>`;
    }
    case "canonical_url": {
      const url = String(d.canonical_url || "");
      if (!/^https?:\/\//i.test(url)) return "<td></td>";
      const kind = /pdf/i.test(d.content_type || "") || /\.pdf(\?|$)/i.test(url) ? "pdf" : "web";
      return `<td><a href="${esc(url)}" rel="noopener nofollow" title="${esc(url)}">${kind}&nbsp;↗</a></td>`;
    }
    default:
      return `<td>${esc(d[key] == null ? "" : d[key])}</td>`;
  }
}

function render() {
  if (!loaded) return; // early clicks must not replace "Loading…" with "0 of 0"
  const rows = filtered();
  const cols = COLUMNS.filter(c => state.visible.has(c.key));

  $("tbl-head").innerHTML = cols.map(c => {
    const active = state.sort.key === c.key;
    const dir = active ? `<span class="dir" aria-hidden="true">${state.sort.dir > 0 ? "▲" : "▼"}</span>` : "";
    const ariaSort = active ? (state.sort.dir > 0 ? "ascending" : "descending") : "none";
    return `<th data-key="${c.key}" aria-sort="${ariaSort}">` +
           `<button type="button" class="sort-btn">${c.label} ${dir}</button></th>`;
  }).join("");
  for (const th of $("tbl-head").querySelectorAll("th")) {
    th.querySelector("button").addEventListener("click", () => {
      const key = th.dataset.key;
      if (state.sort.key === key) state.sort.dir *= -1;
      else state.sort = { key, dir: key === "publication_date" ? -1 : 1 };
      render();
    });
  }

  $("tbl-body").innerHTML = rows.map(d =>
    `<tr>${cols.map(c => cellHtml(d, c.key)).join("")}</tr>`).join("");
  $("count").textContent = `${rows.length} of ${state.docs.length} documents`;
}

function setupControls() {
  $("q").addEventListener("input", e => { state.q = e.target.value; render(); });
  const bind = (id, key) => $(id).addEventListener("change", e => {
    state.facets[key] = e.target.value; render();
  });
  bind("f-independent", "is_independent");
  bind("f-safety", "safety");

  $("clear-filters").addEventListener("click", () => {
    $("q").value = ""; state.q = "";
    $("f-independent").value = ""; state.facets.is_independent = "";
    $("f-safety").value = ""; state.facets.safety = "";
    for (const m of Object.values(msels)) m.clear();
    state.facets.publisher = new Set();
    state.facets.doc_type = new Set();
    state.facets.openness = new Set();
    state.facets.risk = new Set();
    render();
  });

  const boxes = $("column-boxes");
  for (const c of COLUMNS) {
    const label = document.createElement("label");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.checked = state.visible.has(c.key);
    box.addEventListener("change", () => {
      box.checked ? state.visible.add(c.key) : state.visible.delete(c.key);
      render();
    });
    label.append(box, " " + c.label);
    boxes.appendChild(label);
  }

  $("export").addEventListener("click", exportCsv);
}

function exportCsv() {
  const cols = COLUMNS.filter(c => state.visible.has(c.key));
  const quote = v => {
    let s = String(v == null ? "" : v);
    // spreadsheet formula-injection guard for untrusted titles/fields
    if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
    return `"${s.replace(/"/g, '""')}"`;
  };
  const lines = [cols.map(c => quote(c.key)).join(",")];
  for (const d of filtered()) {
    lines.push(cols.map(c => {
      const v = d[c.key];
      return quote(Array.isArray(v) ? v.join("; ") : v);
    }).join(","));
  }
  const blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "cardtrack-export.csv";
  a.click();
  URL.revokeObjectURL(a.href);
}

async function main() {
  setupControls();
  try {
    // no-cache: always revalidate so the table reflects the latest build
    const resp = await fetch("./data/metadata.json", { cache: "no-cache" });
    const data = await resp.json();
    state.docs = data.documents || [];
    state.publishers = data.publishers || {};
    state.riskLabels = data.risk_domains || {};
    loaded = true;
  } catch (e) {
    $("count").textContent = "Failed to load metadata.json";
    return;
  }
  const countBy = key => {
    const m = new Map();
    for (const d of state.docs) {
      const v = d[key];
      if (v) m.set(v, (m.get(v) || 0) + 1);
    }
    return [...m.entries()].sort((a, b) => a[0].localeCompare(b[0]))
      .map(([value, count]) => ({ value, count }));
  };
  msels.publisher = createMsel($("f-publisher"), { label: "publisher",
    onChange: v => { state.facets.publisher = v; render(); } });
  msels.publisher.setOptions(countBy("publisher"));
  msels.doc_type = createMsel($("f-doctype"), { label: "type",
    onChange: v => { state.facets.doc_type = v; render(); } });
  msels.doc_type.setOptions(countBy("doc_type"));

  const opennessCounts = new Map();
  for (const d of state.docs) {
    const v = d.openness || "na";
    opennessCounts.set(v, (opennessCounts.get(v) || 0) + 1);
  }
  msels.openness = createMsel($("f-openness"), { label: "openness",
    onChange: v => { state.facets.openness = v; render(); } });
  msels.openness.setOptions(
    ["restricted", "closed", "open_weight_restrictive", "open_weight_permissive", "na"]
      .filter(v => opennessCounts.has(v))
      .map(v => ({ value: v, label: OPENNESS_LABELS[v], count: opennessCounts.get(v) })));

  const riskCounts = new Map();
  for (const d of state.docs) {
    for (const r of d.risk_domains || []) riskCounts.set(r, (riskCounts.get(r) || 0) + 1);
  }
  msels.risk = createMsel($("f-risk"), { label: "risk",
    onChange: v => { state.facets.risk = v; render(); } });
  // vocabulary order from config, not alphabetical; only tags actually in use
  msels.risk.setOptions(
    Object.keys(state.riskLabels)
      .filter(r => riskCounts.has(r))
      .map(r => ({ value: r, label: state.riskLabels[r], count: riskCounts.get(r) })));
  render();
}

main();
