(() => {
  const formset = document.querySelector("[data-receta-formset]");
  if (!formset) return;

  const totalForms = formset.querySelector('input[name$="-TOTAL_FORMS"]');
  const rows = formset.querySelector("[data-receta-lineas]");
  const emptyForm = formset.querySelector("template[data-receta-linea-vacia]");
  const addButton = formset.querySelector("[data-add-receta-linea]");
  const maxForms = Number.parseInt(formset.dataset.maxForms, 10) || 10;

  if (!totalForms || !rows || !emptyForm || !addButton) return;

  const syncButton = () => {
    addButton.disabled = Number.parseInt(totalForms.value, 10) >= maxForms;
  };

  addButton.addEventListener("click", () => {
    const index = Number.parseInt(totalForms.value, 10);
    if (index >= maxForms) return;

    const rowHtml = emptyForm.innerHTML.replaceAll("__prefix__", String(index));
    rows.insertAdjacentHTML("beforeend", rowHtml);
    totalForms.value = String(index + 1);
    syncButton();
  });

  syncButton();
})();
