const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

test('la notificación muestra entradas como texto, sin interpretarlas como HTML', () => {
  let appended;
  const nodes = { '.title': {}, '.message': {} };
  const toast = { innerHTML: '', querySelector: selector => nodes[selector] };
  const context = {
    document: { querySelector: () => ({ appendChild: element => { appended = element; } }), createElement: () => toast },
    setTimeout: () => 0,
  };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(__dirname + '/mensajes.js', 'utf8'), context);
  context.success('<img src=x onerror="alert(1)">');
  assert.equal(appended, toast);
  assert.equal(nodes['.message'].textContent, '<img src=x onerror="alert(1)">');
  assert.equal(nodes['.title'].textContent, 'Éxito');
  assert.equal(toast.innerHTML.includes('onerror'), false);
});

test('una página sin contenedor de notificaciones no falla', () => {
  const context = { document: { querySelector: () => null }, setTimeout: () => 0 };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(__dirname + '/mensajes.js', 'utf8'), context);
  assert.doesNotThrow(() => context.warning('Texto'));
});
