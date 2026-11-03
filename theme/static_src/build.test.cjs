const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

test('un fallo del compilador conserva la hoja CSS anterior', () => {
  const output = path.resolve(__dirname, '../static/css/dist/styles.css');
  const previous = fs.readFileSync(output);
  let status;
  const requireMock = name => name === 'node:child_process' ? { spawnSync: () => ({ status: 1 }) } : require(name);
  requireMock.resolve = require.resolve;
  const code = fs.readFileSync(__dirname + '/build.cjs', 'utf8');
  const context = { __dirname, require: requireMock, process: {
    execPath: process.execPath, env: process.env,
    exit: code => { status = code; throw new Error('fin esperado'); }
  } };
  assert.throws(() => vm.runInNewContext(code, context), /fin esperado/);
  assert.equal(status, 1);
  assert.deepEqual(fs.readFileSync(output), previous);
});

test('una compilación sin utilidades conserva el CSS anterior aunque el CLI devuelva éxito', () => {
  const output = path.resolve(__dirname, '../static/css/dist/styles.css');
  const previous = fs.readFileSync(output);
  let status, removed = false;
  const fsMock = { ...fs,
    readFileSync: (file, ...args) => file === output + '.tmp' ? '.incompleto{}' : fs.readFileSync(file, ...args),
    unlinkSync: file => { assert.equal(file, output + '.tmp'); removed = true; }
  };
  const requireMock = name => name === 'node:fs' ? fsMock : name === 'node:child_process' ? { spawnSync: () => ({ status: 0 }) } : require(name);
  requireMock.resolve = require.resolve;
  const context = { __dirname, require: requireMock, console: { error() {} }, process: {
    execPath: process.execPath, env: process.env,
    exit: code => { status = code; throw new Error('fin esperado'); }
  } };
  assert.throws(() => vm.runInNewContext(fs.readFileSync(__dirname + '/build.cjs', 'utf8'), context), /fin esperado/);
  assert.equal(status, 1);
  assert.equal(removed, true);
  assert.deepEqual(fs.readFileSync(output), previous);
});
