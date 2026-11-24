"""Respaldo y activación autorizada de FarmaTEF.0011, sin inspeccionar filas."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DESTINO = ROOT / 'db.sqlite3'
CARPETA = ROOT / '.test-artifacts' / 'sala036'
MANIFIESTO = CARPETA / 'respaldo.json'
TARGET = ('FarmaTEFApp', '0011_sala_farmacia')


def conectar_lectura(path):
    return sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)


def verificar_integridad(path):
    with conectar_lectura(path) as db:
        resultado = db.execute('PRAGMA quick_check').fetchall()
    if resultado != [('ok',)]:
        raise SystemExit('La integridad SQLite no es correcta; no continuar.')
    return 'ok'


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def respaldo():
    if not DESTINO.is_file():
        raise SystemExit('La base local esperada no existe.')
    CARPETA.mkdir(parents=True, exist_ok=True)
    if MANIFIESTO.exists():
        raise SystemExit('Ya existe un manifiesto de esta operación; preservarlo.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    archivo = CARPETA / f'db.sqlite3.before-sala036-{stamp}'
    verificar_integridad(DESTINO)
    with conectar_lectura(DESTINO) as source, sqlite3.connect(archivo) as target:
        source.backup(target)
    metadata = {'origen': str(DESTINO), 'respaldo': str(archivo),
                'bytes': archivo.stat().st_size, 'sha256': sha256(archivo),
                'quick_check': verificar_integridad(archivo), 'migracion': list(TARGET),
                'autorizacion': 'Usuaria: autorizo; 2026-11-24', 'aplicada': False}
    MANIFIESTO.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return metadata


def cargar_respaldo():
    metadata = json.loads(MANIFIESTO.read_text(encoding='utf-8'))
    archivo = Path(metadata['respaldo']).resolve()
    if archivo.parent != CARPETA.resolve() or Path(metadata['origen']).resolve() != DESTINO.resolve():
        raise SystemExit('Destino o respaldo inesperados.')
    if sha256(archivo) != metadata['sha256'] or verificar_integridad(archivo) != 'ok':
        raise SystemExit('El respaldo cambió; no aplicar.')
    return metadata


aplicar = '--apply' in sys.argv
metadata = cargar_respaldo() if aplicar else respaldo()
os.environ['CLINITENS_READ_ENV'] = '0'
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.local_runtime'
import django
django.setup()
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
if Path(settings.DATABASES['default']['NAME']).resolve() != DESTINO.resolve():
    raise SystemExit('La configuración no apunta a la base local autorizada.')
executor = MigrationExecutor(connection)
plan = [(m.app_label, m.name, backwards) for m, backwards in executor.migration_plan([TARGET])]
print(json.dumps({'respaldo': metadata['respaldo'], 'bytes': metadata['bytes'],
                  'quick_check': metadata['quick_check'], 'sha256': metadata['sha256'],
                  'plan': plan}), flush=True)
if plan not in ([(*TARGET, False)], []):
    raise SystemExit('El plan incluye cambios distintos de 0011; se detiene sin migrar.')
if aplicar:
    if plan:
        call_command('migrate', *TARGET, interactive=False, verbosity=1)
    executor = MigrationExecutor(connection)
    if executor.migration_plan([TARGET]):
        raise SystemExit('La migración no quedó aplicada.')
    requeridas = {'FarmaTEFApp_salafarmacia', 'FarmaTEFApp_mueblefarmacia', 'FarmaTEFApp_ubicacionmedicamento'}
    if not requeridas.issubset(set(connection.introspection.table_names())):
        raise SystemExit('Faltan tablas esperadas de la sala.')
    connection.close()
    metadata.update(aplicada=True, quick_check_posterior=verificar_integridad(DESTINO),
                    verificada_en=datetime.now(timezone.utc).isoformat())
    MANIFIESTO.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps({'migracion_aplicada': list(TARGET), 'tablas_verificadas': sorted(requeridas),
                      'quick_check_posterior': metadata['quick_check_posterior']}), flush=True)
