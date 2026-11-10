/* Mejora progresiva del select: sus opciones y permisos siguen siendo del servidor. */
(() => {
  let sequence = 0;
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  function enhance(select) {
    if (select.dataset.searchReady || select.closest('template')) return;
    select.dataset.searchReady = '1';
    const id = select.id || `medicamento-${++sequence}`;
    if (!select.id) select.id = id;
    const labels = [...select.labels];
    const name = labels.map(label => label.textContent.trim()).join(' ') || 'Medicamento';
    const wrapper = document.createElement('div'); wrapper.className = 'medicine-picker';
    select.before(wrapper); wrapper.append(select);
    const input = document.createElement('input'); input.type = 'text';
    input.id = id + '-search'; input.className = 'input'; input.autocomplete = 'off';
    input.placeholder = 'Escribe el nombre o principio activo';
    input.setAttribute('role', 'combobox'); input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    const list = document.createElement('div'); list.id = id + '-options';
    list.className = 'medicine-options'; list.setAttribute('role', 'listbox'); list.setAttribute('aria-label', name);
    list.hidden = true; input.setAttribute('aria-controls', list.id);
    const status = document.createElement('p'); status.id = id + '-status'; status.className = 'medicine-status';
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    input.setAttribute('aria-describedby', [select.getAttribute('aria-describedby'), status.id].filter(Boolean).join(' '));
    if (select.hasAttribute('aria-invalid')) input.setAttribute('aria-invalid', select.getAttribute('aria-invalid'));
    input.required = select.required; select.required = false;
    labels.forEach(label => { label.htmlFor = input.id; });
    if (!labels.length) input.setAttribute('aria-label', name);
    const toggle = document.createElement('button'); toggle.type = 'button'; toggle.className = 'medicine-toggle';
    toggle.textContent = '▾'; toggle.setAttribute('aria-label', 'Mostrar opciones de ' + name);
    toggle.setAttribute('aria-controls', list.id);
    wrapper.append(input, toggle, list, status); select.hidden = true;
    let active = -1, shown = [];
    const options = () => [...select.options].filter(option => option.value && !option.disabled && !option.hidden);
    function close() { list.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; }
    function sync() {
      input.value = select.value ? select.selectedOptions[0]?.textContent || '' : '';
      input.disabled = select.disabled; toggle.disabled = select.disabled; input.setCustomValidity('');
    }
    function highlight(index) {
      active = index;
      [...list.children].forEach((el, i) => el.setAttribute('aria-selected', String(i === active)));
      if (active >= 0) { input.setAttribute('aria-activedescendant', list.children[active].id); list.children[active].scrollIntoView({block: 'nearest'}); }
    }
    function choose(option) {
      select.value = option.value; sync(); close(); input.focus();
      select.dispatchEvent(new Event('change', {bubbles: true}));
    }
    function render(query) {
      const terms = normalize(query).trim().split(/\s+/).filter(Boolean);
      const matches = options().filter(option => terms.every(term => normalize(option.dataset.search || option.textContent).includes(term)));
      shown = matches.slice(0, 20); active = -1; list.replaceChildren(); input.removeAttribute('aria-activedescendant');
      shown.forEach((option, index) => {
        const row = document.createElement('button'); row.type = 'button'; row.tabIndex = -1;
        row.id = `${id}-option-${index}`; row.setAttribute('role', 'option'); row.setAttribute('aria-selected', 'false');
        row.textContent = option.textContent;
        const details = [option.dataset.principio, option.dataset.concentracion, option.dataset.forma].filter(Boolean).join(' · ');
        if (details) { const detail = document.createElement('small'); detail.textContent = details; row.append(detail); }
        row.addEventListener('mousedown', event => event.preventDefault());
        row.addEventListener('click', () => choose(option)); list.append(row);
      });
      status.textContent = matches.length ? `${matches.length} coincidencias${matches.length > 20 ? '; se muestran las primeras 20. Escribe más para afinar la búsqueda.' : '. Elige una opción de la lista.'}` : 'Sin coincidencias. Prueba otro nombre o principio activo.';
      list.hidden = !shown.length; input.setAttribute('aria-expanded', String(shown.length > 0));
    }
    input.addEventListener('focus', () => { input.select(); render(''); });
    input.addEventListener('input', () => {
      if (select.value) { select.value = ''; select.dispatchEvent(new Event('change', {bubbles: true})); }
      input.setCustomValidity(input.value.trim() ? 'Elige un medicamento de las coincidencias.' : '');
      render(input.value);
    });
    input.addEventListener('keydown', event => {
      if (event.key === 'Escape') { close(); return; }
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault(); if (list.hidden) render(input.value);
        if (shown.length) highlight(active < 0 ? (event.key === 'ArrowDown' ? 0 : shown.length - 1) : (active + (event.key === 'ArrowDown' ? 1 : -1) + shown.length) % shown.length);
      } else if (event.key === 'Enter' && !list.hidden && active >= 0) { event.preventDefault(); choose(shown[active]); }
      else if (event.key === 'Tab') close();
    });
    toggle.addEventListener('click', () => { const wasOpen = !list.hidden; input.focus(); if (wasOpen) close(); else render(''); });
    wrapper.addEventListener('focusout', event => { if (!wrapper.contains(event.relatedTarget)) close(); });
    // Los cambios del select producidos externamente también actualizan el texto.
    select.addEventListener('change', () => {
      if (select.value) sync();
      else if (!wrapper.contains(document.activeElement)) sync();
    });
    select.form?.addEventListener('reset', () => setTimeout(() => { sync(); close(); status.textContent = ''; }, 0));
    sync();
  }
  const scan = root => root.querySelectorAll('select[data-medicamento-search]').forEach(enhance);
  document.addEventListener('DOMContentLoaded', () => {
    scan(document);
    new MutationObserver(records => {
      for (const record of records) for (const node of record.addedNodes) if (node.nodeType === 1) {
        if (node.matches('select[data-medicamento-search]')) enhance(node); else scan(node);
      }
    }).observe(document.body, {childList: true, subtree: true});
  });
})();
