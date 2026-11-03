const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

// Ejecuta el controlador real de la plantilla con respuestas controladas.
function fixture() {
  const pending = [];
  let create;
  const context = {
    document: { addEventListener: (_, init) => init() },
    Alpine: { data: (_, factory) => { create = factory; } },
    fetch: () => new Promise((resolve, reject) => pending.push({ resolve, reject })),
    alert() {},
  };
  const template = fs.readFileSync(path.join(__dirname, '../../templates/pages/clinitens/docente/pacientes.html'), 'utf8');
  const script = template.match(/<script>([\s\S]*?)<\/script>/)[1];
  vm.runInNewContext(script, context);
  const state = create();
  state.$refs = { detalle: { open: false, showModal() { this.open = true; }, close() { this.open = false; } } };
  return { state, pending };
}
const response = name => ({ ok: true, json: async () => ({ nombre: name }) });

test('una respuesta antigua no sobrescribe al paciente abierto después', async () => {
  const { state, pending } = fixture();
  const first = state.abrir('/alfa');
  state.cerrar();
  const second = state.abrir('/beta');
  pending[1].resolve(response('Beta'));
  await second;
  pending[0].resolve(response('Alfa'));
  await first;
  assert.equal(state.paciente.nombre, 'Beta');
  assert.equal(state.abierto, true);
});

test('un fallo antiguo no cierra una consulta nueva ni oculta su carga', async () => {
  const { state, pending } = fixture();
  const first = state.abrir('/alfa');
  state.cerrar();
  const second = state.abrir('/beta');
  pending[0].reject(new Error('Red interrumpida'));
  await first;
  assert.equal(state.abierto, true);
  assert.equal(state.cargando, true);
  pending[1].resolve(response('Beta'));
  await second;
  assert.equal(state.paciente.nombre, 'Beta');
});

test('cerrar durante la carga impide que la respuesta repueble el modal cerrado', async () => {
  const { state, pending } = fixture();
  const request = state.abrir('/alfa');
  state.cerrar();
  pending[0].resolve(response('Alfa'));
  await request;
  assert.equal(state.paciente, null);
  assert.equal(state.abierto, false);
  assert.equal(state.cargando, false);
});

test('errores HTTP y de red dejan un error visible y permiten cerrar y reabrir', async () => {
  for (const http of [true, false]) {
    const { state, pending } = fixture();
    const request = state.abrir('/alfa');
    if (http) pending[0].resolve({ ok: false });
    else pending[0].reject(new Error('Error de red'));
    await request;
    assert.equal(state.abierto, true);
    assert.equal(state.cargando, false);
    assert.match(state.error, /No fue posible cargar/);
    state.cerrar();
    const next = state.abrir('/beta');
    assert.equal(state.error, '');
    pending[1].resolve(response('Beta'));
    await next;
    assert.equal(state.paciente.nombre, 'Beta');
  }
});

test('el cierre exterior distingue el fondo de los bordes y el contenido del diálogo', async () => {
  const { state, pending } = fixture();
  const request = state.abrir('/alfa');
  const dialog = state.$refs.detalle;
  dialog.getBoundingClientRect = () => ({ left: 16, right: 374, top: 16, bottom: 828 });
  state.cerrarFuera({ target: dialog, clientX: 20, clientY: 20 });
  assert.equal(state.abierto, true);
  state.cerrarFuera({ target: {}, clientX: 100, clientY: 200 });
  assert.equal(state.abierto, true);
  state.cerrarFuera({ target: dialog, clientX: 5, clientY: 200 });
  assert.equal(state.abierto, false);
  assert.equal(dialog.open, false);
  pending[0].resolve(response('Alfa'));
  await request;
  assert.equal(state.paciente, null);
});
