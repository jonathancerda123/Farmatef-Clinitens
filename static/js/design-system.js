/* Interacciones de presentación; no altera formularios, datos ni permisos. */
document.addEventListener("DOMContentLoaded", () => {
  const navigation = document.querySelector(".app-navigation");
  const desktop = window.matchMedia("(min-width: 1024px)");
  function syncNavigation() { if (navigation) navigation.open = desktop.matches; }
  syncNavigation();
  desktop.addEventListener("change", syncNavigation);
  const disclosures = [...document.querySelectorAll("details[data-disclosure]")];
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    for (const item of disclosures) {
      if (!item.open || (item === navigation && desktop.matches)) continue;
      item.open = false;
      if (item.contains(document.activeElement)) item.querySelector("summary").focus();
    }
  });
  document.addEventListener("click", (event) => {
    for (const item of disclosures) {
      if (item.open && !item.contains(event.target) && !(item === navigation && desktop.matches)) item.open = false;
    }
  });
  let fieldCounter = 0;
  function enhanceFields(root) {
    for (const label of root.querySelectorAll("label:not([for])")) {
      if (label.querySelector("input,select,textarea")) continue;
      const next = label.nextElementSibling;
      const control = next?.matches("input,select,textarea") ? next : next?.querySelector("input:not([type=hidden]),select,textarea");
      if (!control) continue;
      if (!control.id) control.id = "clinical-field-" + (++fieldCounter);
      label.htmlFor = control.id;
    }
    for (const control of root.querySelectorAll("input[id],select[id],textarea[id]")) {
      const error = document.getElementById(control.id + "_error") || document.getElementById("error_1_" + control.id);
      if (!error) continue;
      const describedBy = new Set((control.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean));
      describedBy.add(error.id);
      control.setAttribute("aria-describedby", [...describedBy].join(" "));
      control.setAttribute("aria-invalid", "true");
    }
    for (const table of root.querySelectorAll("table")) {
      for (const header of table.querySelectorAll("thead th")) if (!header.hasAttribute("scope")) header.scope = "col";
      for (const row of table.querySelectorAll("tbody tr")) {
        for (const control of row.querySelectorAll("input:not([type=hidden]),textarea,select")) {
          if (control.labels?.length || control.hasAttribute("aria-label")) continue;
          const cell = control.closest("td");
          const header = table.querySelectorAll("thead th")[cell?.cellIndex];
          if (header) control.setAttribute("aria-label", header.textContent.trim() + ", fila " + row.rowIndex);
        }
      }
    }
  }
  enhanceFields(document);
  const workspace = document.querySelector(".workspace-content");
  if (workspace) new MutationObserver(records => {
    for (const record of records) if ([...record.addedNodes].some(node => node.nodeType === 1)) {
      enhanceFields(workspace); break;
    }
  }).observe(workspace, {childList: true, subtree: true});
});
