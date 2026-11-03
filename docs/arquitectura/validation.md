# Validación documental — 2026-10-28

Estado: artefacto generado y validaciones automatizadas aprobadas. Aceptación humana pendiente.

## Entorno y comandos ejecutados

- Node.js v24.22.1, Archify 3.0.1; sin instalar dependencias.
- `node .codex/skills/archify/bin/archify.mjs doctor`: código 0; recursos, renderizadores, esquemas y validadores incluidos correctos. doctor no constituye prueba de detección Chrome.
- ARCHIFY_CHROME ausente del entorno del proceso. El browser-check encontró automáticamente `C:\Program Files\Google\Chrome\Application\chrome.exe` (chrome.status=available). No se modificó ninguna variable ni archivo de configuración.
- Primera ejecución restringida de finalize: código 1 por EPERM al resolver identidad de ruta; ninguna validación ejecutada en ese intento.
- Reintento con permisos ampliados de ejecución: finalize/showcase código 0. Validaciones aprobadas; recomendación de revisar dos cruces cerca de SQLite.
- Se conservó candidate.primera-version.json. Se amplió solamente la altura del nodo SQLite y se ajustó su posición para mantener el centro. Semántica intacta.
- Comando final (desde raíz):

```powershell
node .codex/skills/archify/bin/archify.mjs finalize architecture docs/arquitectura/candidate.json docs/arquitectura/clinitens.html --quality showcase --out-dir docs/arquitectura/review-2 --json
```

Resultado final: código 0; validate, deliver, check y browser-check PASS; diagnostics vacío. Recibo definitivo: review-2/clinitens.finalize-summary.json. Los recibos de raíz corresponden al primer candidato y son históricos; la entrega vigente está vinculada en clinitens.delivery.json.

Chrome: contención y legibilidad PASS a 1440×900, 1600×1000, 1920×1080 y 2048×1320 en tema claro, sin overflow horizontal. El desplazamiento vertical del lector es aceptado por Archify. No se revisaron capturas perceptualmente; visualReview=not-requested. No se afirma validación móvil ni de tema oscuro.

## Integridad y límites

candidate.json SHA-256: 51431f0e15acbb7e4f15a08bc1e0011546ff2f7b300a3f41e3e306290dfea6dc.
clinitens.html SHA-256: b6550fc38360613a0b5593a961db043da70c35e2bb708a1d07a91e579c0cfb01.

Copia sin .git; no se ejecutó verificación de evidencia contra revisión Git ni se usó --repo-root. Fuentes y huellas locales en FUENTES.md y fuentes.sha256.json. No se ejecutó Django, pruebas de negocio o migraciones ni se accedió a secretos/base/medios. No se modificó código ni configuración. Archify detectó una actualización 3.2.0 y no se instaló.

## Próximo paso

Abrir clinitens.html en Chrome y revisar contenido/legibilidad con el equipo. Si se requiere evidencia vinculada a commit, repetir desde un checkout real con identidad Git verificable. Esta documentación no cambia la aceptación pendiente de 005/006 ni el estado operativo del producto.
