# Inventario de dependencias — 004

Consulta y verificación: 2026-10-08, America/Santiago (evidencia UTC incluida). Base Git `main/e56913c`, inicialmente limpia. Actualización autorizada por el usuario. [Informe global](VALIDACION_PREPRODUCCION.md).

La columna «declarada» compara los pins originales con `requirements.txt` actual. «Instalada» corresponde a `.test-artifacts/dependencias-004/target`, medida con pip list; **`.venv` original conserva las versiones anteriores**. El método existente es un freeze plano: fija también transitivas y herramientas de desarrollo. No se convirtió a otro gestor.

## Python: todos los 54 pins actuales

Django 5.2.18 LTS se elige frente a la última rama 6.1.2 por soporte prolongado hasta abril de 2028 y compatibilidad del proyecto. La rama 5.1 dejó de estar soportada. [Calendario oficial](https://www.djangoproject.com/download/), [anuncio LTS](https://www.djangoproject.com/weblog/2025/apr/02/django-52-released/). Las versiones exactas consultadas proceden de PyPI; una página de documentación puede mostrar un patch anterior al registro.

| Paquete / ámbito / tipo | Declarada inicial → final | Instalada evaluada | Última estable | Candidata compatible | Avisos / decisión | Fuente |
|---|---|---|---|---|---|---|
| argon2-cffi / producción/directa | 25.1.0 → 25.1.0 | 25.1.0 | 25.1.0 | 25.1.0 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/argon2-cffi/json) |
| argon2-cffi-bindings / transitiva fijada | 25.1.0 → 26.1.0 | 26.1.0 | 26.1.0 | 26.1.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/argon2-cffi-bindings/json) |
| arrow / transitiva fijada | 1.3.0 → 1.4.0 | 1.4.0 | 1.4.0 | 1.4.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/arrow/json) |
| asgiref / transitiva fijada | 3.8.1 → 3.12.1 | 3.12.1 | 3.12.1 | 3.12.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/asgiref/json) |
| binaryornot / transitiva fijada | 0.4.4 → 0.6.0 | 0.6.0 | 0.6.0 | 0.6.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/binaryornot/json) |
| black / desarrollo/directa | 24.10.0 → 26.10.0 | 26.10.0 | 26.10.0 | 26.10.0 | 2 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/black/json) |
| certifi / transitiva fijada | 2024.8.30 → 2026.7.22 | 2026.7.22 | 2026.7.22 | 2026.7.22 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/certifi/json) |
| cffi / transitiva fijada | 1.17.1 → 2.1.1 | 2.1.1 | 2.1.1 | 2.1.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/cffi/json) |
| chardet / transitiva fijada | 5.2.0 → 7.6.0 | 7.6.0 | 7.6.0 | 7.6.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/chardet/json) |
| charset-normalizer / transitiva fijada | 3.4.0 → 3.5.2 | 3.5.2 | 3.5.2 | 3.5.2 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/charset-normalizer/json) |
| click / transitiva fijada | 8.1.7 → 8.5.0 | 8.5.0 | 8.5.0 | 8.5.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/click/json) |
| colorama / transitiva fijada | 0.4.6 → 0.4.6 | 0.4.6 | 0.4.6 | 0.4.6 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/colorama/json) |
| cookiecutter / desarrollo/directa | 2.6.0 → 2.7.1 | 2.7.1 | 2.7.1 | 2.7.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/cookiecutter/json) |
| crispy-tailwind / producción/directa | 1.0.3 → 1.0.3 | 1.0.3 | 1.0.3 | 1.0.3 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/crispy-tailwind/json) |
| cryptography / transitiva fijada | no instalada → 50.0.2 | 50.0.2 | 50.0.2 | 50.0.2 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/cryptography/json) |
| django / producción/directa | 5.1.2 → 5.2.18 | 5.2.18 | 6.1.2 | 5.2.18 | 22 avisos iniciales deduplicados → 0 en pip-audit final; rama LTS soportada | [PyPI](https://pypi.org/pypi/Django/json) |
| django-allauth / producción/directa | 0.62.1 → 65.19.7 | 65.19.7 | 65.19.7 | 65.19.7 | 3 avisos iniciales deduplicados → 0 en pip-audit final; extra [mfa]; configuración de login y formularios MFA adaptados | [PyPI](https://pypi.org/pypi/django-allauth/json) |
| django-axes / producción/directa | 6.4.0 → 8.3.1 | 8.3.1 | 8.3.1 | 8.3.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/django-axes/json) |
| django-ckeditor-5 / producción/directa | 0.2.20 → 0.2.20 | 0.2.20 | 0.2.20 | 0.2.20 | Sin avisos en conjunto final; wrapper vigente; aviso JS incorporado separado abajo | [PyPI](https://pypi.org/pypi/django-ckeditor-5/json) |
| django-crispy-forms / producción/directa | 2.3 → 2.7 | 2.7 | 2.7 | 2.7 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/django-crispy-forms/json) |
| django-environ / producción/directa | 0.11.2 → 0.14.0 | 0.14.0 | 0.14.0 | 0.14.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/django-environ/json) |
| django-preventconcurrentlogins / producción/directa | 0.8.2 → 0.8.2 | 0.8.2 | 0.8.2 | 0.8.2 | Sin avisos en conjunto final; conservar última estable y AutoField original mediante AppConfig; invalidación de sesión anterior comprobada | [PyPI](https://pypi.org/pypi/django-preventconcurrentlogins/json) |
| django-tailwind / producción/directa | 3.8.0 → 4.5.0 | 4.5.0 | 4.5.0 | 4.5.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/django-tailwind/json) |
| et-xmlfile / transitiva fijada | 2.0.0 → 2.0.0 | 2.0.0 | 2.0.0 | 2.0.0 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/et_xmlfile/json) |
| fido2 / transitiva fijada | no instalada → 2.2.1 | 2.2.1 | 2.2.1 | 2.2.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/fido2/json) |
| idna / transitiva fijada | 3.10 → 3.20 | 3.20 | 3.20 | 3.20 | 1 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/idna/json) |
| jinja2 / transitiva fijada | 3.1.4 → 3.1.6 | 3.1.6 | 3.1.6 | 3.1.6 | 3 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/Jinja2/json) |
| markdown-it-py / transitiva fijada | 3.0.0 → 4.2.0 | 4.2.0 | 4.2.0 | 4.2.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/markdown-it-py/json) |
| markupsafe / transitiva fijada | 3.0.2 → 3.0.4 | 3.0.4 | 3.0.4 | 3.0.4 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/MarkupSafe/json) |
| mdurl / transitiva fijada | 0.1.2 → 0.1.2 | 0.1.2 | 0.1.2 | 0.1.2 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/mdurl/json) |
| mypy-extensions / transitiva fijada | 1.0.0 → 1.1.0 | 1.1.0 | 1.1.0 | 1.1.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/mypy-extensions/json) |
| nh3 / producción/directa | 0.3.7 → 0.3.7 | 0.3.7 | 0.3.7 | 0.3.7 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/nh3/json) |
| openpyxl / producción/directa | 3.1.5 → 3.1.5 | 3.1.5 | 3.1.5 | 3.1.5 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/openpyxl/json) |
| packaging / transitiva fijada | 24.1 → 26.3 | 26.3 | 26.3 | 26.3 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/packaging/json) |
| pathspec / transitiva fijada | 0.12.1 → 1.1.1 | 1.1.1 | 1.1.1 | 1.1.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/pathspec/json) |
| pillow / producción/directa | 11.3.0 → 12.3.0 | 12.3.0 | 12.3.0 | 12.3.0 | 18 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/pillow/json) |
| platformdirs / transitiva fijada | 4.3.6 → 4.12.4 | 4.12.4 | 4.12.4 | 4.12.4 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/platformdirs/json) |
| pycparser / transitiva fijada | 2.22 → 3.1 | 3.1 | 3.1 | 3.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/pycparser/json) |
| pygments / transitiva fijada | 2.18.0 → 2.21.0 | 2.21.0 | 2.21.0 | 2.21.0 | 1 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/Pygments/json) |
| pytailwindcss / transitiva fijada | no instalada → 0.3.1 | 0.3.1 | 0.3.1 | 0.3.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/pytailwindcss/json) |
| python-dateutil / transitiva fijada | 2.9.0.post0 → 2.9.0.post0 | 2.9.0.post0 | 2.9.0.post0 | 2.9.0.post0 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/python-dateutil/json) |
| python-slugify / transitiva fijada | 8.0.4 → 9.1.3 | 9.1.3 | 9.1.3 | 9.1.3 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/python-slugify/json) |
| pytokens / transitiva fijada | no instalada → 0.4.1 | 0.4.1 | 0.4.1 | 0.4.1 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/pytokens/json) |
| pyyaml / transitiva fijada | 6.0.2 → 6.0.3 | 6.0.3 | 6.0.3 | 6.0.3 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/PyYAML/json) |
| qrcode / transitiva fijada | 8.0 → 8.2 | 8.2 | 8.2 | 8.2 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/qrcode/json) |
| reportlab / producción/directa | 5.0.1 → 5.0.1 | 5.0.1 | 5.0.1 | 5.0.1 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/reportlab/json) |
| requests / transitiva fijada | 2.32.3 → 2.34.2 | 2.34.2 | 2.34.2 | 2.34.2 | 2 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/requests/json) |
| rich / transitiva fijada | 13.9.2 → 15.0.0 | 15.0.0 | 15.0.0 | 15.0.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/rich/json) |
| six / transitiva fijada | 1.16.0 → 1.17.0 | 1.17.0 | 1.17.0 | 1.17.0 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/six/json) |
| sqlparse / transitiva fijada | 0.5.1 → 0.6.0 | 0.6.0 | 0.6.0 | 0.6.0 | 6 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/sqlparse/json) |
| text-unidecode / transitiva fijada | 1.3 → 1.3 | 1.3 | 1.3 | 1.3 | Sin avisos en conjunto final; conservar última estable | [PyPI](https://pypi.org/pypi/text-unidecode/json) |
| types-python-dateutil / transitiva fijada | 2.9.0.20241003 → 2.9.0.20260807 | 2.9.0.20260807 | 2.9.0.20260807 | 2.9.0.20260807 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/types-python-dateutil/json) |
| tzdata / transitiva fijada | 2024.2 → 2026.5 | 2026.5 | 2026.5 | 2026.5 | Sin avisos en conjunto final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/tzdata/json) |
| urllib3 / transitiva fijada | 2.2.3 → 2.8.0 | 2.8.0 | 2.8.0 | 2.8.0 | 8 avisos iniciales deduplicados → 0 en pip-audit final; actualizar; instalación/pip check/regresiones correctos | [PyPI](https://pypi.org/pypi/urllib3/json) |

Conjunto resuelto completo: [inicial](evidencias/004-dependencias/python-inicial.json), [final](evidencias/004-dependencias/python-final.json), [resolución con hashes de ruedas](evidencias/004-dependencias/python-resolucion.json), [consulta oficial](evidencias/004-dependencias/pypi-consulta.json). Pip es herramienta del entorno, no pin de producción: inicial 23.2.1, objetivo 26.2.1.

## Frontend directo: actual y retirado

Tailwind 4.3.3 usa CLI separado, @import/@source explícitos y config JS de compatibilidad. Se conservan tokens, formularios y typography. Requiere navegadores modernos: Chrome 111+, Safari 16.4+, Firefox 128+. [Guía oficial](https://tailwindcss.com/docs/upgrade-guide). Alpine/DOMPurify ya estaban en su última versión y se sirven localmente.

| Paquete / ámbito / tipo | Declarada inicial → final | Instalada evaluada | Última estable | Candidata compatible | Avisos / decisión | Fuente |
|---|---|---|---|---|---|---|
| @tailwindcss/aspect-ratio / frontend, desarrollo-build directa | ^0.4.2 → retirada | no instalada | 0.4.2 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/%40tailwindcss%2Faspect-ratio) |
| @tailwindcss/cli / frontend, desarrollo-build directa | ausente → 4.3.3 | 4.3.3 | 4.3.3 | 4.3.3 | 0 avisos en lock final; build verificado | [npm](https://registry.npmjs.org/%40tailwindcss%2Fcli) |
| @tailwindcss/forms / frontend, desarrollo-build directa | ^0.5.7 → 0.5.11 | 0.5.11 | 0.5.11 | 0.5.11 | 0 avisos en lock final; build verificado | [npm](https://registry.npmjs.org/%40tailwindcss%2Fforms) |
| @tailwindcss/typography / frontend, desarrollo-build directa | ^0.5.10 → 0.5.20 | 0.5.20 | 0.5.20 | 0.5.20 | 0 avisos en lock final; build verificado | [npm](https://registry.npmjs.org/%40tailwindcss%2Ftypography) |
| alpinejs / frontend, desarrollo-build directa | 3.17.4 → 3.17.4 | 3.17.4 | 3.17.4 | 3.17.4 | 0 avisos en lock final; conservar recurso local | [npm](https://registry.npmjs.org/alpinejs) |
| cross-env / frontend, desarrollo-build directa | ^7.0.3 → retirada | no instalada | 10.1.0 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/cross-env) |
| dompurify / frontend, desarrollo-build directa | 3.4.16 → 3.4.16 | 3.4.16 | 3.4.16 | 3.4.16 | 0 avisos en lock final; conservar recurso local | [npm](https://registry.npmjs.org/dompurify) |
| postcss / frontend, desarrollo-build directa | ^8.4.32 → retirada | no instalada | 8.5.29 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/postcss) |
| postcss-import / frontend, desarrollo-build directa | ^15.1.0 → retirada | no instalada | 17.0.0 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/postcss-import) |
| postcss-nested / frontend, desarrollo-build directa | ^6.0.1 → retirada | no instalada | 8.0.1 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/postcss-nested) |
| postcss-simple-vars / frontend, desarrollo-build directa | ^7.0.1 → retirada | no instalada | 7.0.1 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/postcss-simple-vars) |
| rimraf / frontend, desarrollo-build directa | ^5.0.5 → retirada | no instalada | 6.1.3 | retirada | Retirar: flujo de build ya no lo usa; aspecto nativo en Tailwind 4 | [npm](https://registry.npmjs.org/rimraf) |
| tailwindcss / frontend, desarrollo-build directa | ^3.4.0 → 4.3.3 | 4.3.3 | 4.3.3 | 4.3.3 | 0 avisos en lock final; build verificado | [npm](https://registry.npmjs.org/tailwindcss) |

Overrides de compatibilidad auditados: `@parcel/watcher==2.6.0` sustituye el árbol que trae braces <=3.0.3 (sin patch publicado); `postcss-selector-parser==7.1.6` bajo typography sustituye 6.0.10. Build, watch y uso de prose comprobados. No se instaló `--force`. [Braces](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm), [selector parser](https://github.com/advisories/GHSA-rj75-hqrm-r3gf).

Transitivas completas y hashes: [package-lock](../theme/static_src/package-lock.json), [árbol instalado](evidencias/004-dependencias/npm-final-resuelto.json), [lock inicial](evidencias/004-dependencias/npm-inicial.json). Opcionales de otras plataformas presentes en lock pueden no estar instaladas en Windows; no se equiparan ambos inventarios.

## Recursos externos y editor incorporado

El escaneo de src/href de templates detectó **0 recursos CDN externos**. No hay actualización de URLs CDN que aplicar: las fuentes, Alpine, DOMPurify y el editor son locales. [Escaneo](evidencias/004-dependencias/recursos-externos.json).

| Recurso / tipo | Declarada | Instalada/servida evaluada | Última/candidata | Avisos y decisión | Fuente / evidencia |
|---|---|---|---|---|---|
| Alpine / JS local | 3.17.4 | 3.17.4 | 3.17.4 | Conservada, fijada y copiada en build | [npm](evidencias/004-dependencias/npm-consulta.json) |
| DOMPurify / JS local | 3.4.16 | 3.4.16 | 3.4.16 | Conservada, fijada y copiada con licencia | [npm](evidencias/004-dependencias/npm-consulta.json) |
| CKEditor / bundle del wrapper | django-ckeditor-5 0.2.20 | CKEDITOR_VERSION 47.5.0 | Wrapper 0.2.20 vigente; corrección JS >=47.6.0 | Un aviso distinto CVE-2026-28343/GHSA-jrqm-vmqc-gm93. No se habilita HTML inseguro en configuración actual; no se demuestra explotación. Pendiente bundle corregido por proveedor o integración mantenida aparte | [Aviso oficial](https://github.com/advisories/GHSA-jrqm-vmqc-gm93), [firma/manifest](evidencias/004-dependencias/ckeditor-proveedor.json), [lock/auditoría](evidencias/004-dependencias/ckeditor-lock-audit.json) |

El lock incluido por el proveedor identifica 176 paquetes runtime y las 39 dependencias directas de su build. Se conservan todas las versiones resueltas, consulta de últimas directas y respuesta npm en `ckeditor-lock-audit.json`. Dos entradas (ckeditor5 y html-support) corresponden al **mismo** GHSA/CVE y se cuentan una sola vez. No se instaló el toolchain ni se reconstruyó el bundle del proveedor; el lock y firma no demuestran que todas sus funciones se ejecuten. Inspector se identifica por su versión real 5.0.0 en el lock, no por la firma común 47.5.0 del editor.

## Runtime y herramientas

| Componente | Instalado evaluado | Última estable consultada / candidata | Decisión / soporte / límite | Fuente |
|---|---|---|---|---|
| Python | 3.12.0, base de .venv y target | 3.14.8 estable anunciada; rama 3.12: 3.12.15 | Rama 3.12 con soporte de seguridad hasta octubre 2028, pero patch instalado antiguo. 3.12.15 es solo fuentes; en Windows valorar binario 3.13.16/3.14.8 y repetir suite. No se cambió intérprete del sistema ni se validaron esas versiones | [Python oficial](https://blog.python.org/2026/10/python-31022-31117/) |
| Node | 24.15.0 | 26.11.1 Current / 24.21.0 LTS | Build compatible con 24 probado; actualizar patch LTS del sistema antes de reutilizar CI. engines admite ramas soportadas 22/24. No se instaló runtime global | [Node oficial](https://nodejs.org/en/download) |
| npm | 11.12.1 | No consultada por separado | Herramienta usada para instalación, lock y audit; no dependencia servida | Salidas de comandos |
| pip-audit | 2.10.1, entorno audit-tools | No se persigue última por rutina | Herramienta aislada; servicio PyPI vulnerabilities; no agregada a requirements | [Herramienta](https://github.com/pypa/pip-audit) |
| PDF QA | pypdf 6.10.0, Poppler del runtime Codex | No consultada | Solo inspección de exportación ficticia; no dependencia de app | [Exportaciones](evidencias/004-dependencias/exportaciones.json) |

## Resultado de auditoría

- Inicial Python: 118 registros de avisos en 10 paquetes; **66 avisos distintos** al unir alias CVE/GHSA/PYSEC. Final: 0 avisos conocidos para los 54 pins resueltos. [Inicial](evidencias/004-dependencias/pip-audit-inicial.json), [deduplicados](evidencias/004-dependencias/avisos-python-deduplicados.json), [final](evidencias/004-dependencias/pip-audit-final.json).
- npm del proyecto: inicialmente 8 paquetes afectados (5 altos, 3 moderados); final 0. [Inicial](evidencias/004-dependencias/npm-audit-inicial.json), [final](evidencias/004-dependencias/npm-audit-final.json).
- Editor incorporado: un aviso distinto moderado pendiente; no queda cubierto por pip-audit ni por el lock npm del tema. Se revisó por separado.
- [Comandos, códigos de salida y tiempos finales](evidencias/004-dependencias/auditorias-final-metadatos.json). pip check verifica consistencia; no busca vulnerabilidades. Cero avisos del auditor no certifica ausencia de vulnerabilidades ni parcheo del runtime.

Se auditaron conjuntos exactos, sin --fix y con herramienta separada. Se mantiene resolución/hash en evidencia y pins/lock existentes; requirements no usa --require-hashes. No se atribuye explotación a ninguno de los avisos.
