/* Checkbox-dropdown multi-select, shared by the table (app.js) and search page.
   Markup contract:
   <details class="msel"><summary></summary><div class="msel-panel"></div></details> */
"use strict";

function createMsel(root, { label, onChange }) {
  const summary = root.querySelector("summary");
  const panel = root.querySelector(".msel-panel");
  const selected = new Set();

  function refresh() {
    summary.classList.toggle("active", selected.size > 0);
    summary.textContent = !selected.size ? `${label}: all`
      : selected.size === 1 ? `${label}: ${[...selected][0]}`
      : `${label}: ${selected.size} selected`;
  }

  function setOptions(options) {
    // options: [{value, count?}]; selections that no longer exist are dropped
    for (const v of [...selected]) if (!options.some(o => o.value === v)) selected.delete(v);
    panel.innerHTML = "";
    const clear = document.createElement("button");
    clear.type = "button";
    clear.className = "msel-clear";
    clear.textContent = "clear";
    clear.addEventListener("click", () => {
      selected.clear();
      for (const box of panel.querySelectorAll("input")) box.checked = false;
      refresh();
      onChange(new Set(selected));
    });
    panel.appendChild(clear);
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
      lab.append(box, ` ${o.value}`);
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
  return { setOptions, get selected() { return new Set(selected); } };
}

// one open dropdown at a time; clicking elsewhere closes it
document.addEventListener("click", e => {
  for (const d of document.querySelectorAll("details.msel[open]")) {
    if (!d.contains(e.target)) d.open = false;
  }
});
