(() => {
  const cargo = document.getElementById("id_position_FK");
  const contenedor = document.querySelector("[data-area-docente]");
  if (!cargo || !contenedor) return;
  const area = contenedor.querySelector("select");

  function actualizarArea() {
    const docente = cargo.selectedOptions[0]?.dataset.docente === "true";
    contenedor.hidden = !docente;
    area.disabled = !docente;
    area.required = docente;
  }

  cargo.addEventListener("change", actualizarArea);
  actualizarArea();
})();
