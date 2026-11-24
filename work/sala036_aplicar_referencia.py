"""Aplicar SAL-09 a una sala local explícita; sin copiar stock ni recetas."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
AREA=ROOT/'.test-artifacts'/'sala036-distribucion'
BASE=ROOT/'db.sqlite3'
MANIFEST=AREA/'operacion.json'


def integridad(path):
    with sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True) as db:
        if db.execute('PRAGMA quick_check').fetchall()!=[('ok',)]:
            raise RuntimeError('Integridad SQLite incorrecta.')
    return 'ok'


def hash_archivo(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            digest.update(chunk)
    return digest.hexdigest()


def referencia():
    def item(number,tipo,nombre,x,y,w,h,d,filas=1,columnas=1,orientacion=0):
        return dict(id=-number,tipo=tipo,nombre=nombre,x_cm=x,y_cm=y,ancho_cm=w,alto_cm=h,
                    fondo_cm=d,filas=filas,columnas=columnas,orientacion=orientacion)
    muebles=[item(i+1,'sliding',f'Estante {i+1}',60+140*i,20,140,190,60,7,3)for i in range(4)]
    muebles += [item(5,'counter','Mesón de trabajo',80,125,560,90,70),
                item(6,'board','Pizarra',15,220,180,100,5,orientacion=270)]
    muebles += [item(7+i,'studentTable',f'Mesa {i+1}',110+(i%2)*410,260+(i//2)*210,180,75,90)for i in range(6)]
    muebles += [item(13,'entrance','Entrada principal',1010,700,160,200,90,orientacion=90)]
    return dict(ancho_cm=1100,largo_cm=900,muebles=muebles)


parser=argparse.ArgumentParser()
parser.add_argument('accion',choices=['ensayar','aplicar'])
parser.add_argument('--propietario',type=int,required=True)
parser.add_argument('--version',type=int,required=True)
args=parser.parse_args()

if args.accion=='ensayar':
    AREA.mkdir(parents=True,exist_ok=True)
    if MANIFEST.exists():
        raise SystemExit('Ya existe una operación de referencia; preservar el respaldo y sus metadatos.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup=AREA/f'db.sqlite3.before-distribucion-{stamp}'
    integridad(BASE)
    with sqlite3.connect(BASE.resolve().as_uri()+'?mode=ro',uri=True) as origen,sqlite3.connect(backup) as destino:
        origen.backup(destino)
    integridad(backup)
    ensayo=AREA/f'ensayo-{stamp}.sqlite3'
    shutil.copyfile(backup,ensayo)
    meta=dict(propietario_id=args.propietario,version_previa=args.version,respaldo=str(backup),
              bytes=backup.stat().st_size,sha256=hash_archivo(backup),quick_check='ok',
              ensayo=str(ensayo),aplicada=False,autorizacion='Solicitud explícita SAL-09 de reproducir imagen en proyecto local')
    MANIFEST.write_text(json.dumps(meta,indent=2),encoding='utf8')
    database=ensayo
else:
    meta=json.loads(MANIFEST.read_text(encoding='utf8'))
    backup=Path(meta['respaldo']).resolve()
    if backup.parent!=AREA.resolve() or args.propietario!=meta['propietario_id'] or args.version!=meta['version_previa']:
        raise SystemExit('El propietario, versión o respaldo no corresponden al ensayo.')
    if meta['aplicada'] or not meta.get('ensayo_correcto') or hash_archivo(backup)!=meta['sha256']:
        raise SystemExit('Operación ya aplicada, ensayo incompleto o respaldo modificado.')
    integridad(backup)
    database=BASE

os.environ['CLINITENS_READ_ENV']='0'
os.environ['DJANGO_SETTINGS_MODULE']='core.local_runtime'
from django.conf import settings
settings.DATABASES['default']['NAME']=database
import django
django.setup()
from django.contrib.auth import get_user_model
from django.db import connection,transaction
from FarmaTEFApp.models import SalaFarmacia,UbicacionMedicamento
from FarmaTEFApp.sala import guardar_sala,CAMPOS_MUEBLE

if Path(connection.settings_dict['NAME']).resolve()!=database.resolve():
    raise SystemExit('Destino de base inesperado.')
owner=get_user_model().objects.get(pk=args.propietario,is_active=True)
with transaction.atomic():
    sala=SalaFarmacia.objects.filter(propietario=owner).first()
    actual_version=sala.version if sala else 0
    if actual_version!=args.version:
        raise RuntimeError('La sala cambió después de la inspección; no sobrescribir.')
    anteriores=list(sala.muebles.all()) if sala else []
    ubicaciones_antes=list(UbicacionMedicamento.objects.filter(mueble__sala=sala).order_by('pk').values_list('pk','mueble_id','compartimento')) if sala else []
    payload=referencia()
    usados=set()
    for m in payload['muebles']:
        candidatos=[o for o in anteriores if o.tipo==m['tipo'] and o.pk not in usados]
        candidato=next((o for o in candidatos if o.nombre==m['nombre']),candidatos[0] if candidatos else None)
        if candidato:
            m['id']=candidato.pk
            usados.add(candidato.pk)
            if m['tipo'] in ('sliding','drawers'):
                m['filas'],m['columnas']=candidato.filas,candidato.columnas
    sala=guardar_sala(owner,owner,json.dumps(payload),args.version)
    ubicaciones_despues=list(UbicacionMedicamento.objects.filter(mueble__sala=sala).order_by('pk').values_list('pk','mueble_id','compartimento'))
    if ubicaciones_antes!=ubicaciones_despues:
        raise RuntimeError('Las asignaciones cambiaron; se revierte la distribución.')
    reales=list(sala.muebles.order_by('pk').values(*CAMPOS_MUEBLE))
    esperados=[{k:m[k]for k in CAMPOS_MUEBLE}for m in payload['muebles']]
    if sorted(reales,key=lambda m:m['nombre'])!=sorted(esperados,key=lambda m:m['nombre']) or (sala.ancho_cm,sala.largo_cm)!=(1100,900):
        raise RuntimeError('La geometría no coincide con la referencia; se revierte.')
connection.close()
resultado=dict(destino='copia de ensayo' if args.accion=='ensayar' else 'base local autorizada',
               sala_cm=[1100,900],muebles=13,version=sala.version,ubicaciones_conservadas=len(ubicaciones_despues),
               integridad=integridad(database),respaldo=meta['respaldo'],sha256=meta['sha256'])
if args.accion=='ensayar':
    meta['ensayo_correcto']=True
    meta['resultado_ensayo']=resultado
else:
    meta['aplicada']=True
    meta['resultado_local']=resultado
    meta['aplicada_en']=datetime.now(timezone.utc).isoformat()
MANIFEST.write_text(json.dumps(meta,indent=2),encoding='utf8')
print(json.dumps(resultado,ensure_ascii=False),flush=True)
