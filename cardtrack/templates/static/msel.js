/* Checkbox-dropdown multi-select, shared by the table (app.js) and search page.
   Markup contract:
   <details class="msel"><summary></summary><div class="msel-panel"></div></details> */
"use strict";

function createMsel(root, { label, onChange }) {
  const summary = root.querySelector("summary");
  const panel = root.querySelector(".msel-panel");
  const selected = new Set();
  let labels = new Map();

  function refresh() {
    summary.classList.toggle("active", selected.size > 0);
    const name = v => labels.get(v) ?? v;
    summary.textContent = !selected.size ? `${label}: all`
      : selected.size === 1 ? `${label}: ${name([...selected][0])}`
      : `${label}: ${selected.size} selected`;
  }

  // silent reset: callers decide whether to re-render (the panel's own clear
  // button fires onChange; a page-level "clear filters" resets state itself)
  function clear() {
    selected.clear();
    for (const box of panel.querySelectorAll("input")) box.checked = false;
    refresh();
  }

  function setOptions(options) {
    // options: [{value, label?, count?}]; selections that no longer exist are dropped
    for (const v of [...selected]) if (!options.some(o => o.value === v)) selected.delete(v);
    labels = new Map(options.map(o => [o.value, o.label ?? o.value]));
    panel.innerHTML = "";
    const clearBtn = document.createElement("button");
    clearBtn.type = "button";
    clearBtn.className = "msel-clear";
    clearBtn.textContent = "clear";
    clearBtn.addEventListener("click", () => {
      clear();
      onChange(new Set(selected));
    });
    panel.appendChild(clearBtn);
    for (const o of options) {
      const lab = document.createElement("label");
      const box = document.createElement("input");
      box.type = "checkbox";
      box.value = o.value;
      box.checked = selected.has(o.value);
      box.addEventListener("change", () => {
        if (box.checked) selected.add(o.value); else selected.delete(o.value);
        refresh();
        onChange(new Set(selected));
      });
      lab.append(box, ` ${o.label ?? o.value}`);
      if (o.count != null) {
        const c = document.createElement("span");
        c.className = "msel-count";
        c.textContent = o.count;
        lab.appendChild(c);
      }
      panel.appendChild(lab);
    }
    refresh();
  }

  refresh();
  return { setOptions, clear, get selected() { return new Set(selected); } };
}

// one open dropdown at a time; clicking elsewhere closes it
document.addEventListener("click", e => {
  for (const d of document.querySelectorAll("details.msel[open]")) {
    if (!d.contains(e.target)) d.open = false;
  }
});
