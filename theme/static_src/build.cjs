const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const output = path.resolve(__dirname, '../static/css/dist/styles.css');
const temporary = output + '.tmp';
const assets = [
  ['alpinejs/dist/cdn.min.js', 'alpine.min.js'], ['dompurify/dist/purify.min.js', 'purify.min.js'],
  ['dompurify/LICENSE', 'DOMPURIFY-LICENSE.txt']
].map(([source, target]) => [fs.readFileSync(path.join(__dirname, 'node_modules', source)), target]);
fs.mkdirSync(path.dirname(output), { recursive: true });
const cliPackage = require.resolve('@tailwindcss/cli/package.json');
const cli = path.resolve(path.dirname(cliPackage), require(cliPackage).bin.tailwindcss);
const result = spawnSync(process.execPath, [cli,
  '-i', './src/styles.css', '-o', temporary, '--minify'], {
  cwd: __dirname, stdio: 'inherit', env: { ...process.env, NODE_ENV: 'production' }
});
if (result.status !== 0 || result.error) {
  if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
  process.exit(result.status || 1);
}
// El escáner nativo puede omitir fuentes sin devolver error si no puede leerlas.
// Estas utilidades se usan en la interfaz y deben estar presentes antes de publicar.
const compiled = fs.readFileSync(temporary, 'utf8');
if (!['.sr-only{', '.hidden{', '.grid{', '.w-full{'].every(selector => compiled.includes(selector))) {
  fs.unlinkSync(temporary);
  console.error('Tailwind no generó las utilidades esperadas. Revisar acceso a las fuentes @source; se conserva el CSS anterior.');
  process.exit(1);
}
const vendor = path.resolve(__dirname, '../../static/vendor');
fs.mkdirSync(vendor, { recursive: true });
for (const [contents, target] of assets) fs.writeFileSync(path.join(vendor, target), contents);
fs.renameSync(temporary, output);
