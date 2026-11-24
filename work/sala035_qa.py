"""Servidor de revisión, exclusivamente datos ficticios en .test-artifacts."""
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
browser_mode='--browser' in sys.argv
port=8036 if browser_mode else 8035
db=ROOT/'.test-artifacts'/('sala035-browser.sqlite3' if browser_mode else 'sala035-qa.sqlite3')
reuse='--reuse' in sys.argv
if db.exists() and not reuse:
    raise SystemExit('La fixture ya existe; conservarla y elegir otra ruta para una nueva carga.')
os.environ['DJANGO_SETTINGS_MODULE']='core.test_settings'
os.environ['CLINITENS_TEST_DATABASE']=str(db)
import django
django.setup()
from django.core.management import call_command
if not reuse:
    call_command('migrate',verbosity=0,interactive=False)
from core.test_helpers import usuario
from FarmaTEFApp.models import Medicamento,LoteInventario,Receta,RecetaLinea
from FarmaTEFApp.sala import guardar_sala,asignar_ubicacion
from CliniTensDocenteApp.models import Curso
from django.utils import timezone
import json
def crear_fixture():
    docente=usuario('qa035-docente','MANAGER',area_docente='FARMACIA')
    alumno=usuario('qa035-alumno')
    curso=Curso.objects.create(nombre='Farmacia QA 035',creado_por=docente);curso.estudiantes.add(alumno)
    receta=Receta.objects.create(numero='QA035-01',persona_ficticia='Persona SIM',creado_por=docente,curso=curso,vence_el=timezone.localdate())
    medicamentos=[]
    for i,nombre in enumerate(['Ácido fólico SIM','Losartán SIM','Metformina SIM','Ibuprofeno SIM']):
        m=Medicamento.objects.create(nombre=nombre,concentracion='Presentación SIM',creado_por=docente);medicamentos.append(m)
        LoteInventario.objects.create(medicamento=m,registrado_por=docente,numero_lote=f'QA035-{i}',vence_el=timezone.localdate(),unidades=25 if i!=2 else 0)
        if i<2:RecetaLinea.objects.create(receta=receta,medicamento=m,unidades=5)
    return docente,alumno,receta,medicamentos
def furniture(i,tipo,nombre,x,y,w,h,d,filas=1,columnas=1,orientacion=0):
    return dict(id=-i,tipo=tipo,nombre=nombre,x_cm=x,y_cm=y,ancho_cm=w,alto_cm=h,fondo_cm=d,filas=filas,columnas=columnas,orientacion=orientacion)
if reuse:
    from django.contrib.auth import get_user_model
    docente=get_user_model().objects.get(username='qa035-docente')
    alumno=get_user_model().objects.get(username='qa035-alumno')
    receta=Receta.objects.get(numero='QA035-01')
else:
    docente,alumno,receta,medicamentos=crear_fixture()
    muebles=[furniture(i+1,'sliding',f'Estante {i+1}',60+140*i,20,140,190,60,7,3)for i in range(4)]
    muebles+=[furniture(5,'counter','Mesón de trabajo',80,125,560,90,70),furniture(6,'board','Pizarra',15,220,180,100,5,orientacion=270)]
    muebles +=[furniture(7+i,'studentTable',f'Mesa {i+1}',110+(i%2)*410,260+(i//2)*210,180,75,90)for i in range(6)]
    sala=guardar_sala(docente,docente,json.dumps(dict(ancho_cm=1000,largo_cm=900,muebles=muebles)),0)
    for med,idx,slot in [(medicamentos[0],0,'A-2'),(medicamentos[1],2,'F2-4'),(medicamentos[2],2,'B-5')]:
        asignar_ubicacion(docente,docente,med.pk,list(sala.muebles.all())[idx].pk,slot,sala.version);sala.refresh_from_db()
from django.conf import settings
from django.urls import include,path
from django.contrib.auth import login
from django.shortcuts import redirect
def qa_docente(request):
    login(request,docente,backend='django.contrib.auth.backends.ModelBackend');return redirect('farmatef:configurar_sala')
def qa_alumno(request):
    login(request,alumno,backend='django.contrib.auth.backends.ModelBackend');return redirect('farmatef:practica_receta',receta_id=receta.pk)
urlpatterns=[path('_qa/035/docente/',qa_docente),path('_qa/035/alumno/',qa_alumno),path('',include('core.urls'))]
settings.ROOT_URLCONF=__name__
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server
print(f'QA035 fixture creada; http://127.0.0.1:{port}/_qa/035/docente/ y /_qa/035/alumno/',flush=True)
make_server('127.0.0.1',port,StaticFilesHandler(get_wsgi_application())).serve_forever()
