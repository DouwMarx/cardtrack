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
  { key: "canonical_url", label: "Source", show: true },
  { key: "status", label: "Status", show: false },
  { key: "version_count", label: "Versions", show: false },
  { key: "first_seen", label: "First seen", show: false },
];

const state = {
  docs: [],
  q: "",
  facets: { publisher: "", doc_type: "", is_independent: "", status: "", year: "", safety: "" },
  sort: { key: "publication_date", dir: -1 },
  visible: new Set(COLUMNS.filter(c => c.show).map(c => c.key)),
};

const $ = id => document.getElementById(id);

function norm(s) { return (s || "").toString().toLowerCase(); }

function docYear(d) { return (d.publication_date || "").slice(0, 4); }

function matches(d) {
  const q = norm(state.q);
  if (q) {
    // metadata scope only: identity fields, not bodies (spec §9)
    const hay = norm(d.title) + " " + norm((d.model_names || []).join(" ")) + " " + norm(d.publisher);
    if (!q.split(/\s+/).every(tok => hay.includes(tok))) return false;
  }
  const f = state.facets;
  if (f.publisher && d.publisher !== f.publisher) return false;
  if (f.doc_type && d.doc_type !== f.doc_type) return false;
  if (f.is_independent !== "" && String(d.is_independent) !== f.is_independent) return false;
  if (f.status && d.status !== f.status) return false;
  if (f.year && docYear(d) !== f.year) return false;
  if (f.safety !== "" && String(d.safety_evals) !== f.safety) return false;
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
    case "status":
      return `<td><span class="badge status-${esc(d.status)}">${esc(d.status)}</span></td>`;
    case "safety_evals": {
      if (d.safety_evals === 1) return '<td><span class="badge safety-yes">yes</span></td>';
      if (d.safety_evals === 0) return '<td><span class="badge safety-no">none</span></td>';
      return '<td><span class="badge">?</span></td>';
    }
    case "publisher": {
      const badge = d.is_independent ? ' <span class="badge independent">indep.</span>' : "";
      return `<td>${esc(d.publisher)}${badge}</td>`;
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

function fillFacet(id, values, labeler) {
  const sel = $(id);
  const keep = sel.value;
  while (sel.options.length > 1) sel.remove(1);
  for (const v of values) {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = labeler ? labeler(v) : v;
    sel.appendChild(opt);
  }
  sel.value = keep;
}

function setupControls() {
  $("q").addEventListener("input", e => { state.q = e.target.value; render(); });
  const bind = (id, key) => $(id).addEventListener("change", e => {
    state.facets[key] = e.target.value; render();
  });
  bind("f-publisher", "publisher");
  bind("f-doctype", "doc_type");
  bind("f-independent", "is_independent");
  bind("f-status", "status");
  bind("f-year", "year");
  bind("f-safety", "safety");

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
    const resp = await fetch("./data/metadata.json");
    const data = await resp.json();
    state.docs = data.documents || [];
  } catch (e) {
    $("count").textContent = "Failed to load metadata.json";
    return;
  }
  const uniq = key => [...new Set(state.docs.map(d => d[key]).filter(Boolean))].sort();
  fillFacet("f-publisher", uniq("publisher"));
  fillFacet("f-doctype", uniq("doc_type"));
  fillFacet("f-status", uniq("status"));
  fillFacet("f-year", [...new Set(state.docs.map(docYear).filter(Boolean))].sort().reverse());
  render();
}

main();
