document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-rut='true']").forEach((input) => {
    input.addEventListener("input", () => {
      const clean = input.value.replace(/[^0-9kK]/g, "").toUpperCase();
      if (clean.length < 2) return;
      const body = clean.slice(0, -1).replace(/^0+/, "") || "0";
      const dv = clean.slice(-1);
      input.value = body.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "-" + dv;
    });
  });
});
