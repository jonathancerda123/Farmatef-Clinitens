document.addEventListener("DOMContentLoaded", () => {
  const fields = {
    pas: document.getElementById("id_pa_sistolica"),
    pad: document.getElementById("id_pa_diastolica"),
    peso: document.getElementById("id_peso"),
    talla: document.getElementById("id_talla"),
    pam: document.getElementById("dau-pam"),
    imc: document.getElementById("dau-imc"),
  };
  const update = () => {
    const pas = Number.parseFloat(fields.pas?.value);
    const pad = Number.parseFloat(fields.pad?.value);
    const peso = Number.parseFloat(fields.peso?.value);
    const talla = Number.parseFloat(fields.talla?.value);
    fields.pam.value = Number.isFinite(pas) && Number.isFinite(pad)
      ? ((pas + (2 * pad)) / 3).toFixed(2) : "";
    fields.imc.value = Number.isFinite(peso) && Number.isFinite(talla) && talla > 0
      ? (peso / ((talla / 100) ** 2)).toFixed(2) : "";
  };
  [fields.pas, fields.pad, fields.peso, fields.talla].forEach((input) => {
    input?.addEventListener("input", update);
  });
  update();
});
