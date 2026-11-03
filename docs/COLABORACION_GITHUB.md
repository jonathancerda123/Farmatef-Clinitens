# Trabajo desde dos equipos

Repositorio compartido: https://github.com/jonathancerda123/Farmatef-Clinitens

Cada equipo mantiene su propia copia del código. GitHub recibe los cambios publicados con Git; abrir la misma cuenta de Codex no sustituye esa sincronización. Cada persona debe usar su propia cuenta de GitHub, con acceso de colaboradora al repositorio cuando corresponda.

## Preparación de un equipo nuevo

Clonar una sola vez y abrir la carpeta resultante como proyecto local en Codex:

```powershell
git clone https://github.com/jonathancerda123/Farmatef-Clinitens.git
cd Farmatef-Clinitens
```

Configurar el nombre y correo propios de Git en ese equipo. Preparar las dependencias siguiendo README.md y docs/ENTORNO_Y_VERIFICACION.md: los entornos virtuales, node_modules, configuración privada, base y medios locales no se descargan del repositorio. El launcher documentado del entorno anterior está roto; no copiar ese entorno entre equipos. Para verificaciones usar core.test_settings y datos ficticios; no aplicar migraciones sobre la base recibida.

## Un cambio por rama

Empezar con el árbol limpio. Si existen cambios pendientes, conservarlos en su rama antes de cambiar a main. Descargar la versión compartida y crear una rama con nombre distinto para cada tarea:

```powershell
git switch main
git pull --ff-only origin main
git switch -c tarea/nombre-del-cambio
```

Trabajar con Codex en esa carpeta y rama, respetando AGENTS.md y la autorización de la spec correspondiente. Revisar los archivos antes de guardar y subir:

```powershell
git status
git diff
git add ruta/del/archivo
git diff --cached
git commit -m "Describe el cambio realizado"
git push -u origin HEAD
```

Reemplazar la ruta de ejemplo por los archivos concretos revisados. Abrir una pull request hacia main en GitHub para que la otra persona revise e integre el cambio. Antes de comenzar la siguiente tarea, repetir la actualización de main.

Coordinar tareas si ambas personas necesitan editar el mismo archivo. Si Git informa conflictos o rechaza la actualización, conservar el trabajo y resolverlo con revisión; no usar push --force ni reset --hard para saltarse el problema.

## Archivos que permanecen locales

No subir .env, credenciales, bases SQLite, media/, entornos virtuales, node_modules, .test-artifacts/, tmp/ ni output/. Compartir el código no comparte usuarios ni registros de la aplicación. Usar datos ficticios propios para desarrollar y probar.

El repositorio es público al preparar esta guía el 2026-11-03: los archivos publicados serán visibles a terceros. Publicar código no despliega Django ni acredita preparación para producción.

## Preparación inicial — 2026-11-03

La solicitud de subir el proyecto para colaborar autoriza la inicialización de Git y el primer commit/push a este repositorio. Esta autorización no amplía el desarrollo funcional ni autoriza despliegue o migración de la base recibida. Se amplían exclusiones para configuración privada, bases auxiliares, dependencias y temporales, conservando los archivos físicos.

La comprobación de conexión remota devolvió cero referencias antes de la preparación. La publicación debe verificarse comparando el commit local con main remoto y revisando el índice para comprobar las exclusiones. Este trabajo de versionado no ejecuta ni sustituye pruebas funcionales del producto.

El primer commit se creó localmente, pero el push sigue pendiente de iniciar sesión en el Git de Windows. La conexión de GitHub de la aplicación no autentica automáticamente los comandos de Git. Desde una terminal interactiva en la carpeta del proyecto, ejecutar `git push -u origin main` y completar la autenticación que solicite GitHub. Después, `git rev-parse HEAD` y `git ls-remote origin refs/heads/main` deben mostrar el mismo identificador de commit.
