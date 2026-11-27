import json
from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.test_helpers import usuario
from .forms import MedicamentoForm
from .models import Medicamento, LoteInventario, MovimientoInventario, Receta, RecetaLinea, Dispensacion
from .movimientos import mover_stock, registrar_alta
from .sala import guardar_sala, alternar_candado
from .services import entregar_receta
from .tests_sala import plano


class ControlInventarioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docente = usuario("control037", "MANAGER", area_docente="FARMACIA")
        cls.ajeno = usuario("ajeno037", "MANAGER")
        cls.alumno = usuario("alumno037")
        cls.admin = usuario("admin037", "ADMIN")
        cls.med = Medicamento.objects.create(nombre="SIM 037", clasificacion="PROA", creado_por=cls.docente)
        cls.lote = LoteInventario.objects.create(medicamento=cls.med, numero_lote="SIM037", unidades=10,
            registrado_por=cls.docente, vence_el=timezone.localdate()+timedelta(days=10))

    def test_candado_persistente_cas_y_post_directo(self):
        sala = guardar_sala(self.docente, self.docente, json.dumps(plano()), 0)
        alternar_candado(self.docente, self.docente, sala.version)
        sala.refresh_from_db()
        self.assertTrue(sala.plano_bloqueado)
        with self.assertRaises(ValidationError):
            guardar_sala(self.docente, self.docente, json.dumps(plano([])), sala.version)
        self.client.force_login(self.docente)
        r = self.client.post(reverse("farmatef:configurar_sala"), {"accion":"guardar_sala", "version":sala.version,"configuracion":json.dumps(plano([]))})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(sala.muebles.count(), 1)
        with self.assertRaises(ValidationError):
            alternar_candado(self.docente, self.docente, sala.version-1)
        with self.assertRaises(PermissionDenied):
            alternar_candado(self.ajeno, self.docente, sala.version)
        alternar_candado(self.docente, self.docente, sala.version)
        sala.refresh_from_db()
        self.assertFalse(sala.plano_bloqueado)

    def test_movimiento_reenvio_y_stock_insuficiente(self):
        op=uuid4()
        m=mover_stock(self.docente,self.lote.pk,"salida",3,"venta","",op)
        self.assertEqual((m.saldo_anterior,m.saldo_posterior),(10,7))
        self.assertEqual(mover_stock(self.docente,self.lote.pk,"salida",3,"venta","",op).pk,m.pk)
        with self.assertRaises(ValidationError):
            mover_stock(self.docente,self.lote.pk,"salida",8,"ajuste","",uuid4())
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades,7)
        self.assertEqual(MovimientoInventario.objects.count(),1)

    def test_rollback_si_falla_historial(self):
        with patch("FarmaTEFApp.movimientos.MovimientoInventario.objects.create", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                mover_stock(self.docente,self.lote.pk,"entrada",2,"ingreso","",uuid4())
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.unidades,10)

    def test_motivos_permisos_y_alta(self):
        for sentido,motivo,obs in [("salida","vencimiento",""),("entrada","venta",""),("entrada","otro","")]:
            with self.assertRaises(ValidationError):
                mover_stock(self.docente,self.lote.pk,sentido,1,motivo,obs,uuid4())
        with self.assertRaises(PermissionDenied):
            mover_stock(self.ajeno,self.lote.pk,"entrada",1,"ingreso","",uuid4())
        lote=LoteInventario(medicamento=self.med,numero_lote="ALTA037",unidades=5,vence_el=timezone.localdate())
        registrar_alta(lote,self.docente)
        self.assertEqual(lote.movimientos.get().saldo_posterior,5)

    def test_dispensacion_registra_salida_y_no_duplica(self):
        receta=Receta.objects.create(numero="037",persona_ficticia="SIM",creado_por=self.docente,vence_el=timezone.localdate())
        linea=RecetaLinea.objects.create(receta=receta,medicamento=self.med,unidades=2)
        entregar_receta(receta.pk,self.docente,{linea.pk:2})
        m=MovimientoInventario.objects.get()
        self.assertEqual((m.motivo,m.cantidad,m.saldo_posterior),("dispensacion",2,8))
        self.assertEqual(m.uso.dispensacion.receta_id,receta.pk)
        with self.assertRaises(ValidationError):
            entregar_receta(receta.pk,self.docente,{linea.pk:2})
        self.assertEqual(MovimientoInventario.objects.count(),1)

    def test_precio_limites_filtro_y_rutas(self):
        for valor in [-1,"1.5",1000000000]:
            form=MedicamentoForm({"nombre":"Nuevo037","precio":valor},actor=self.docente)
            self.assertIn("precio",form.errors)
        self.client.force_login(self.docente)
        url=reverse("farmatef:precio",args=[self.med.pk])
        self.assertEqual(self.client.post(url,{"precio":0}).status_code,302)
        self.med.refresh_from_db()
        self.assertEqual(self.med.precio,0)
        self.assertContains(self.client.get(reverse("farmatef:inventario"),{"clasificacion":"PROA"}),"SIM 037")
        self.assertNotContains(self.client.get(reverse("farmatef:inventario"),{"clasificacion":"CPU"}),"SIM 037")
        self.assertEqual(self.client.get(reverse("farmatef:movimientos")).status_code,200)
        self.client.force_login(self.ajeno)
        self.assertEqual(self.client.post(url,{"precio":4}).status_code,404)
        self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(reverse("farmatef:movimientos")).status_code,403)

    def test_dispensacion_revierte_si_falla_movimiento(self):
        receta=Receta.objects.create(numero="037-ROLL",persona_ficticia="SIM",creado_por=self.docente,vence_el=timezone.localdate())
        linea=RecetaLinea.objects.create(receta=receta,medicamento=self.med,unidades=2)
        with patch("FarmaTEFApp.services.MovimientoInventario.objects.create", side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                entregar_receta(receta.pk,self.docente,{linea.pk:2})
        self.lote.refresh_from_db()
        linea.refresh_from_db()
        self.assertEqual(self.lote.unidades,10)
        self.assertEqual(linea.unidades_entregadas,0)
        self.assertFalse(Dispensacion.objects.exists())

    def test_retiro_vencido_y_admin_sin_edicion_de_stock(self):
        self.lote.vence_el=timezone.localdate()-timedelta(days=1)
        self.lote.save(update_fields=["vence_el"])
        m=mover_stock(self.docente,self.lote.pk,"salida",10,"vencimiento","Retiro SIM",uuid4())
        self.assertEqual(m.saldo_posterior,0)
        from django.contrib import admin
        model_admin=admin.site._registry[MovimientoInventario]
        self.assertFalse(model_admin.has_change_permission(None,m))
        self.assertFalse(model_admin.has_delete_permission(None,m))

    def test_formulario_token_impide_duplicar_y_historial_privado(self):
        from .views_movimientos import MovimientoForm
        token=MovimientoForm(actor=self.docente).initial["token"]
        data={"lote":self.lote.pk,"sentido":"entrada","cantidad":4,"motivo":"ingreso","observacion":"Ingreso SIM", "token":token}
        self.client.force_login(self.docente)
        url=reverse("farmatef:movimientos")
        self.assertEqual(self.client.post(url,data).status_code,302)
        self.assertEqual(self.client.post(url,data).status_code,302)
        self.assertEqual(MovimientoInventario.objects.count(),1)
        self.assertContains(self.client.get(url),"Ingreso SIM")
        self.client.force_login(self.ajeno)
        self.assertNotContains(self.client.get(url),"Ingreso SIM")
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(url),"Ingreso SIM")
