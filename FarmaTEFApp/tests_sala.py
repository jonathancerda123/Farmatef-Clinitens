import json
from datetime import timedelta

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from CliniTensDocenteApp.models import Curso
from core.test_helpers import usuario
from .models import Dispensacion, LoteInventario, Medicamento, MuebleFarmacia, Receta, RecetaLinea, SalaFarmacia, UbicacionMedicamento
from .sala import asignar_ubicacion, datos_sala, guardar_sala


def plano(muebles=None):
    return {"ancho_cm": 1000, "largo_cm": 900, "muebles": muebles if muebles is not None else [{
        "id": -1, "nombre": "Estante 1", "tipo": "sliding", "ancho_cm": 140,
        "alto_cm": 190, "fondo_cm": 60, "x_cm": 20, "y_cm": 20,
        "orientacion": 0, "filas": 7, "columnas": 3,
    }]}


class SalaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docente = usuario("sala-docente", "MANAGER", area_docente="FARMACIA")
        cls.otro = usuario("sala-ajeno", "MANAGER")
        cls.enfermeria = usuario("sala-enfermeria", "MANAGER", area_docente="ENFERMERIA")
        cls.admin = usuario("sala-admin", "ADMIN")
        cls.super = usuario("sala-super", None, is_superuser=True)
        cls.alumno = usuario("sala-alumno")
        cls.ajeno = usuario("sala-no-matriculado")
        cls.curso = Curso.objects.create(nombre="Farmacia ficticia", creado_por=cls.docente)
        cls.curso.estudiantes.add(cls.alumno)
        cls.receta = Receta.objects.create(numero="SALA-01", persona_ficticia="Persona SIM", curso=cls.curso, creado_por=cls.docente, vence_el=timezone.localdate()+timedelta(days=3))
        cls.med = Medicamento.objects.create(nombre="Ácido SIM", creado_por=cls.docente)
        cls.med2 = Medicamento.objects.create(nombre="Segundo SIM", creado_por=cls.docente)
        cls.privado = Medicamento.objects.create(nombre="Privado ajeno", creado_por=cls.otro)
        cls.inactivo = Medicamento.objects.create(nombre="Inactivo", creado_por=cls.docente, activo=False)
        cls.linea = RecetaLinea.objects.create(receta=cls.receta, medicamento=cls.med, unidades=3)
        cls.linea2 = RecetaLinea.objects.create(receta=cls.receta, medicamento=cls.med2, unidades=2)
        cls.lote = LoteInventario.objects.create(medicamento=cls.med, numero_lote="VIGENTE", unidades=3, vence_el=timezone.localdate(), registrado_por=cls.docente)
        cls.lote2 = LoteInventario.objects.create(medicamento=cls.med2, numero_lote="VIGENTE-2", unidades=8, vence_el=timezone.localdate(), registrado_por=cls.docente)
        LoteInventario.objects.create(medicamento=cls.med, numero_lote="VENCIDO", unidades=90, vence_el=timezone.localdate()-timedelta(days=1), registrado_por=cls.docente)

    def setUp(self):
        self.gestion = reverse("farmatef:configurar_sala")
        self.consulta = reverse("farmatef:sala")

    def crear(self):
        sala = guardar_sala(self.docente, self.docente, json.dumps(plano()), 0)
        return sala, sala.muebles.get()

    def guardar_actual(self, sala, datos, version=None):
        return guardar_sala(self.docente, self.docente, json.dumps(datos), sala.version if version is None else version)

    def test_get_no_crea_sala_y_guarda_configuracion(self):
        self.client.force_login(self.docente)
        self.assertContains(self.client.get(self.gestion), "Configuración docente")
        self.assertFalse(SalaFarmacia.objects.exists())
        response = self.client.post(self.gestion, {"accion":"guardar_sala", "version":0, "configuracion":json.dumps(plano())})
        self.assertEqual(response.status_code, 302)
        sala = SalaFarmacia.objects.get()
        self.assertEqual(sala.version, 1)
        self.assertEqual(sala.muebles.get().filas, 7)

    def test_entrada_se_guarda_y_es_visible_al_alumno_sin_almacenamiento(self):
        entry={**plano()["muebles"][0],"tipo":"entrance","nombre":"Entrada principal","ancho_cm":160,"alto_cm":200,"fondo_cm":90,"x_cm":420,"y_cm":810,"filas":1,"columnas":1}
        sala=guardar_sala(self.docente,self.docente,json.dumps(plano([entry])),0)
        zona=sala.muebles.get()
        self.assertEqual(zona.tipo,"entrance")
        data=datos_sala(self.docente)
        self.assertEqual(data["muebles"][0]["compartimentos"],[])
        self.assertEqual(data["muebles"][0]["y_cm"],810)
        with self.assertRaises(ValidationError):
            asignar_ubicacion(self.docente,self.docente,self.med.pk,zona.pk,"C1",1)
        self.client.force_login(self.alumno)
        response=self.client.get(self.consulta)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Entrada principal")
        self.assertNotContains(response,'id="sala-config-form"')
        self.assertEqual(self.client.post(self.consulta,{"tipo":"entrance"}).status_code,405)

    def test_entrada_unica_y_fuera_de_sala_se_rechazan_sin_cambios(self):
        entry={**plano()["muebles"][0],"tipo":"entrance","nombre":"Entrada","ancho_cm":160,"fondo_cm":90,"filas":1,"columnas":1,"x_cm":420,"y_cm":810}
        with self.assertRaisesMessage(ValidationError,"sola zona de entrada"):
            guardar_sala(self.docente,self.docente,json.dumps(plano([entry,{**entry,"id":-2,"x_cm":600}])),0)
        self.assertFalse(SalaFarmacia.objects.exists())
        sala=guardar_sala(self.docente,self.docente,json.dumps(plano([entry])),0)
        data=datos_sala(self.docente)
        data["muebles"][0]["y_cm"]=850
        with self.assertRaises(ValidationError):
            self.guardar_actual(sala,data)
        sala.refresh_from_db();self.assertEqual(sala.version,1)
        self.assertEqual(sala.muebles.get().y_cm,810)

    def test_matriz_gestion_url_directa_y_csrf(self):
        self.assertEqual(self.client.get(self.gestion).status_code, 302)
        for user in (self.docente, self.admin, self.super):
            self.client.force_login(user)
            self.assertEqual(self.client.get(self.gestion, {"docente":self.docente.pk}).status_code, 200)
        for user in (self.otro, self.enfermeria, self.alumno):
            self.client.force_login(user)
            self.assertEqual(self.client.get(self.gestion, {"docente":self.docente.pk}).status_code, 403)
            self.assertEqual(self.client.post(self.gestion, {"accion":"guardar_sala"}).status_code, 403 if user != self.otro else 400)
        c = Client(enforce_csrf_checks=True)
        c.force_login(self.docente)
        self.assertEqual(c.post(self.gestion, {"accion":"guardar_sala"}).status_code, 403)
        with self.assertRaises(PermissionDenied):
            guardar_sala(self.otro, self.docente, json.dumps(plano()), 0)

    def test_guardado_obsoleto_no_cambia_datos(self):
        sala, mueble = self.crear()
        datos = datos_sala(self.docente)
        datos["ancho_cm"] = 1200
        with self.assertRaisesMessage(ValidationError, "otra pestaña"):
            self.guardar_actual(sala, datos, 0)
        sala.refresh_from_db()
        self.assertEqual((sala.version, sala.ancho_cm, sala.muebles.count()), (1,1000,1))

    def test_fuera_limites_tipos_bool_cantidad_y_duplicados(self):
        for mutate in (
            lambda p:p.update(ancho_cm=True), lambda p:p.update(muebles=p["muebles"]*31),
            lambda p:p["muebles"][0].update(x_cm=1000), lambda p:p["muebles"][0].update(tipo="inventado"),
            lambda p:p["muebles"][0].update(ancho_cm="140"), lambda p:p.update(muebles=p["muebles"]*2),
            lambda p:p["muebles"][0].update(columnas=2),
        ):
            datos=plano();mutate(datos)
            with self.assertRaises(ValidationError):
                guardar_sala(self.docente,self.docente,json.dumps(datos),0)
            self.assertFalse(SalaFarmacia.objects.exists(), "Fallo revierte incluso la creación inicial")

    def test_mueble_ajeno_y_asignaciones_cruzadas(self):
        sala,mueble=self.crear()
        ajena=guardar_sala(self.otro,self.otro,json.dumps(plano()),0)
        datos=datos_sala(self.docente);datos["muebles"][0]["id"]=ajena.muebles.get().pk
        with self.assertRaises(ValidationError):self.guardar_actual(sala,datos)
        for med,cajon,key in ((self.privado.pk,mueble.pk,"A-1"),(self.med.pk,ajena.muebles.get().pk,"A-1"),(self.med.pk,mueble.pk,"F4-99")):
            with self.assertRaises(ValidationError):asignar_ubicacion(self.docente,self.docente,med,cajon,key,1)
        sala.refresh_from_db();self.assertEqual(sala.version,1)
        self.assertFalse(UbicacionMedicamento.objects.exists())

    def test_stock_vigente_cero_sin_reparto_automatico(self):
        sala,mueble=self.crear()
        antes=datos_sala(self.docente)["productos"]
        self.assertTrue(all(p["mueble_id"] is None for p in antes))
        asignar_ubicacion(self.docente,self.docente,self.med.pk,mueble.pk,"A-2",1)
        datos=datos_sala(self.docente)
        producto=next(p for p in datos["productos"] if p["id"]==self.med.pk)
        self.assertEqual(producto["stock"],3)
        self.assertEqual(producto["compartimento"],"A-2")
        LoteInventario.objects.filter(pk=self.lote.pk).update(unidades=0)
        producto=next(p for p in datos_sala(self.docente)["productos"] if p["id"]==self.med.pk)
        self.assertEqual(producto["stock"],0);self.assertEqual(producto["mueble_id"],mueble.pk)
        self.assertNotIn(self.inactivo.pk,[p["id"] for p in datos["productos"]])

    def test_asignados_impiden_borrado_reduccion_y_cambio_tipo(self):
        sala,mueble=self.crear();asignar_ubicacion(self.docente,self.docente,self.med.pk,mueble.pk,"F3-7",1)
        sala.refresh_from_db()
        for change in (lambda p:p.update(muebles=[]),lambda p:p["muebles"][0].update(filas=6),lambda p:p["muebles"][0].update(tipo="table",filas=1,columnas=1)):
            datos=datos_sala(self.docente);change(datos)
            with self.assertRaises(ValidationError):self.guardar_actual(sala,datos)
            sala.refresh_from_db();self.assertEqual(sala.version,2)
            self.assertTrue(UbicacionMedicamento.objects.filter(mueble=mueble).exists())

    def test_reubicar_y_varios_productos_en_un_cajon(self):
        sala,mueble=self.crear();asignar_ubicacion(self.docente,self.docente,self.med.pk,mueble.pk,"A-2",1)
        asignar_ubicacion(self.docente,self.docente,self.med2.pk,mueble.pk,"A-2",2)
        self.assertEqual(mueble.ubicaciones.count(),2)
        asignar_ubicacion(self.docente,self.docente,self.med.pk,None,"",3)
        self.assertEqual(mueble.ubicaciones.count(),1)
        with self.assertRaisesMessage(ValidationError,"otra pestaña"):
            asignar_ubicacion(self.docente,self.docente,self.med2.pk,mueble.pk,"B-2",3)

    def test_sillas_orientacion_y_tipos_sin_almacenamiento(self):
        for tipo,w,h,d in (("table",140,75,60),("board",180,100,5),("counter",560,90,70),("studentTable",180,75,90),("drawers",120,180,50)):
            datos=plano();datos["muebles"][0].update(tipo=tipo,ancho_cm=w,alto_cm=h,fondo_cm=d,filas=1,columnas=1)
            sala=guardar_sala(self.otro,self.otro,json.dumps(datos),SalaFarmacia.objects.filter(propietario=self.otro).values_list("version",flat=True).first() or 0)
            # Cada prueba sustituye el mueble anterior sin asignaciones.
            self.assertEqual(sala.muebles.count(),1)
        datos=plano();datos["muebles"][0].update(tipo="studentTable",ancho_cm=180,alto_cm=75,fondo_cm=90,filas=1,columnas=1,y_cm=750)
        with self.assertRaises(ValidationError):guardar_sala(self.docente,self.docente,json.dumps(datos),0)

    def test_consulta_matricula_inventario_y_post_denegado(self):
        self.crear();self.client.force_login(self.alumno)
        response=self.client.get(self.consulta);self.assertEqual(response.status_code,200)
        self.assertNotContains(response,"Privado ajeno");self.assertNotContains(response,"Inactivo")
        self.assertNotContains(response,'id="sala-config-form"');self.assertEqual(response["Cache-Control"],"private, no-store")
        self.assertEqual(self.client.post(self.consulta).status_code,405)
        for params in ({"docente":self.otro.pk},{"curso":"x"},{"curso":9999}):self.assertEqual(self.client.get(self.consulta,params).status_code,404)
        self.curso.estudiantes.remove(self.alumno)
        self.assertEqual(self.client.get(self.consulta,{"curso":self.curso.pk}).status_code,404)

    def test_colaborador_no_recibe_inventario_del_otro(self):
        self.curso.docentes_colaboradores.add(self.otro);self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(self.consulta,{"docente":self.otro.pk}).status_code,404)
        self.client.force_login(self.otro);self.assertEqual(self.client.get(self.gestion,{"docente":self.docente.pk}).status_code,403)

    def dispensar(self):
        self.client.force_login(self.alumno)
        return self.client.post(reverse("farmatef:responder_receta",args=[self.receta.pk]),{"decision":"DISPENSAR",f"lote_{self.linea.pk}":self.lote.pk,f"lote_{self.linea2.pk}":self.lote2.pk})

    def test_dispensar_redirige_varios_productos_y_get_no_repite_consumo(self):
        sala,mueble=self.crear();asignar_ubicacion(self.docente,self.docente,self.med.pk,mueble.pk,"A-2",1)
        response=self.dispensar();disp=Dispensacion.objects.get();destino=reverse("farmatef:localizar_dispensacion",args=[disp.pk])
        self.assertRedirects(response,destino)
        for _ in range(2):
            pagina=self.client.get(destino);self.assertEqual(set(pagina.context["datos_sala"]["objetivos"]),{self.med.pk,self.med2.pk})
            self.assertContains(pagina,"Ubicación pendiente")
        self.lote.refresh_from_db();self.assertEqual(self.lote.unidades,0);self.assertEqual(Dispensacion.objects.count(),1)
        self.client.force_login(self.ajeno);self.assertEqual(self.client.get(destino).status_code,404)
        self.client.force_login(self.alumno);self.curso.estudiantes.remove(self.alumno);self.assertEqual(self.client.get(destino).status_code,404)

    def test_dispensacion_sin_sala_es_consultable_y_rechazo_no_localiza(self):
        response=self.dispensar();self.assertEqual(response.status_code,302)
        self.assertContains(self.client.get(response.url),"Ubicación pendiente")
        self.assertFalse(SalaFarmacia.objects.exists())

    def test_rechazo_correcto_no_redirige_al_plano(self):
        self.client.force_login(self.alumno);Receta.objects.filter(pk=self.receta.pk).update(motivo_rechazo_esperado="OTRO")
        response=self.client.post(reverse("farmatef:responder_receta",args=[self.receta.pk]),{"decision":"RECHAZAR","motivo_rechazo":"OTRO","explicacion_otro_motivo":"Caso de prueba"})
        self.assertRedirects(response,reverse("farmatef:practica_receta",args=[self.receta.pk]));self.assertFalse(Dispensacion.objects.exists())

    def test_html_json_seguro_y_compatibilidad_vitrina(self):
        self.crear();self.med.nombre='</script><img src=x onerror="alert(1)">';self.med.save(update_fields=["nombre"])
        self.client.force_login(self.alumno);response=self.client.get(self.consulta)
        self.assertNotContains(response,"<img src=x");self.assertContains(response,r"\u003C/script\u003E")
        self.assertContains(response,"Medicamentos y ubicaciones guardadas")
        self.assertRedirects(self.client.get(reverse("farmatef:vitrina")),self.consulta)

    def test_ajax_error_conserva_version_y_permite_guardado_correcto(self):
        self.client.force_login(self.docente)
        response=self.client.post(self.gestion,{"accion":"guardar_sala","version":0,"configuracion":"[]"},HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code,400);self.assertIn("error",response.json());self.assertFalse(SalaFarmacia.objects.exists())
        response=self.client.post(self.gestion,{"accion":"guardar_sala","version":0,"configuracion":json.dumps(plano())},HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code,200);self.assertIn("url",response.json())
