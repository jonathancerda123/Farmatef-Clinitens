from CliniTensFichaApp.validation import seccion_completa
from core.permissions import (
    es_administrador,
    es_docente,
    objetos_del_docente,
)
from core.mixins import PropietarioMixin, FormularioDocenteMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages
from core.mixins import PermitsPositionMixin
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
    DetailView,
)
from django.db.models.deletion import ProtectedError
from .forms import (
    CasoClinicoForm,
    CodigoActividadForm,
    PacienteForm,
    ResultadoDiagnosticoForm,
    CursoForm,
    CursoColaboradorForm,
    ImportarEstudiantesExcelForm,
)
from .models import (
    CasoClinico,
    CasoMultimedia,
    CodigoActividad,
    Paciente,
    PacienteMultimedia,
    ResultadoDiagnostico,
    Curso,
)
from django.views import View
from django.http import JsonResponse
from CliniTensFichaApp.models import FichaClinica

from html import escape
from django.db.models import Q
from django.http import HttpResponse, Http404

import json

from CliniTensFichaApp.ficha_config import (
    SECCIONES,
    HENDERSON,
    MASLOW,
    GCS,
    DOWNTON,
    BRADEN,
)

from .rubrica import RUBRICA, niveles_por_puntaje
from UsuarioApp.models import Profile
import secrets
import string
import unicodedata
from io import BytesIO
from django.contrib.auth.models import User
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


### En vivo
SECCIONES_FICHA = [
    "identidad",
    "farmacos",
    "signos",
    "recontroles",
    "necesidades",
    "plan",
    "registro",
    "riesgos",
    "balance",
    "examenes",
    "dispositivos",
    "indicaciones",
    "evolucion",
]




#################################  PDF
ETIQUETAS_FICHA = {
    "nombre": "Nombre",
    "nombre_social": "Nombre social",
    "edad": "Edad",
    "sexo": "Sexo biológico",
    "rut": "RUT / Número de identificación",
    "diagnostico": "Diagnóstico médico",
    "patologia": "Descripción y causas de la patología",
    "anamnesis_remota": "Anamnesis remota",
    "anamnesis_proxima": "Anamnesis próxima",
    "filas": "Registros",
    "justificacion": "Justificación / observaciones clínicas",
    "rol_asistencial": "Rol asistencial",
    "rol_administrativo": "Rol administrativo",
    "rol_educativo": "Rol educativo",
}


def fichas_visibles_para(usuario):
    fichas = FichaClinica.objects.select_related(
        "estudiante", "docente", "codigo_actividad__caso_clinico")
    return objetos_del_docente(fichas, usuario, campo="docente")



def nombre_campo(clave):
    return ETIQUETAS_FICHA.get(clave, clave.replace("_", " ").capitalize())


def texto_valor(valor):
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    if isinstance(valor, list):
        if not valor:
            return "Sin información"
        return " · ".join(str(item) for item in valor)

    return str(valor) if valor not in [None, ""] else "Sin información"


def preparar_secciones_ficha(datos):
    datos = datos or {}
    resultado = []

    for clave, _, titulo in SECCIONES:
        contenido = datos.get(clave)

        if not contenido:
            continue

        filas = []

        if isinstance(contenido, dict):
            for campo, valor in contenido.items():
                if isinstance(valor, list) and valor and isinstance(valor[0], dict):
                    for numero, fila in enumerate(valor, start=1):
                        detalle = " · ".join(
                            f"{nombre_campo(llave)}: {texto_valor(dato)}"
                            for llave, dato in fila.items()
                            if dato not in [None, ""]
                        )
                        filas.append((f"Registro {numero}", detalle))
                else:
                    filas.append((nombre_campo(campo), texto_valor(valor)))
        else:
            filas.append(("Información", texto_valor(contenido)))

        resultado.append(
            {
                "clave": clave,
                "titulo": titulo,
                "filas": filas,
            }
        )

    return resultado


######################### NOTAS


#######################  CURSO


def normalizar_encabezado(valor):
    texto = str(valor or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.replace("_", " ").replace("-", " ")
    texto = " ".join(texto.split())

    equivalencias = {
        "username": "username",
        "usuario": "username",
        "nombre usuario": "username",
        "nombre de usuario": "username",
        "email": "email",
        "correo": "email",
        "correo electronico": "email",
        "direccion correo electronico": "email",
        "direccion de correo electronico": "email",
        "first name": "first_name",
        "first_name": "first_name",
        "nombre": "first_name",
        "nombres": "first_name",
        "last name": "last_name",
        "last_name": "last_name",
        "apellido": "last_name",
        "apellidos": "last_name",
    }

    return equivalencias.get(texto, texto)


def generar_contrasena_temporal(longitud=14):
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = "!@#$%*-_"

    caracteres = [
        secrets.choice(mayusculas),
        secrets.choice(minusculas),
        secrets.choice(numeros),
        secrets.choice(simbolos),
    ]

    todos = mayusculas + minusculas + numeros + simbolos

    for _ in range(longitud - len(caracteres)):
        caracteres.append(secrets.choice(todos))

    secrets.SystemRandom().shuffle(caracteres)

    return "".join(caracteres)




############################


class CursoListCreateView(PermitsPositionMixin, ListView):
    model = Curso
    template_name = "pages/clinitens/docente/cursos.html"
    context_object_name = "cursos"

    def get_queryset(self):
        return (
            objetos_del_docente(Curso.objects.all(), self.request.user)
            .annotate(total_estudiantes=Count("estudiantes"))
            .order_by("nombre")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", CursoForm())
        return context

    def post(self, request, *args, **kwargs):
        form = CursoForm(request.POST)

        if form.is_valid():
            curso = form.save(commit=False)
            curso.creado_por = request.user
            curso.save()

            messages.success(request, f'Curso "{curso.nombre}" creado correctamente.')
            return redirect("clinitensdocente:curso_detalle", pk=curso.pk)

        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))


class CursoDetalleView(PermitsPositionMixin, DetailView):
    model = Curso
    template_name = "pages/clinitens/docente/curso_detalle.html"
    context_object_name = "curso"

    def get_queryset(self):
        return objetos_del_docente(Curso.objects.all(), self.request.user).prefetch_related(
            "estudiantes__profile__position_FK"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        termino_busqueda = self.request.GET.get("buscar", "").strip()

        # Estudiantes ya relacionados a este curso.
        estudiantes_curso = (
            self.object.estudiantes.filter(
                is_active=True,
            )
            .select_related("profile", "profile__position_FK")
            .order_by("first_name", "last_name", "username")
        )

        # Estudiantes disponibles para añadir manualmente.
        estudiantes_disponibles = (
            User.objects.filter(
                is_active=True,
                profile__position_FK__permission_code__iexact="RESTRICTED",
            )
            .exclude(pk__in=self.object.estudiantes.values_list("pk", flat=True))
            .select_related("profile", "profile__position_FK")
            .order_by("first_name", "last_name", "username")
        )

        # No listar todos de inmediato: se muestran al buscar.
        if termino_busqueda:
            estudiantes_disponibles = estudiantes_disponibles.filter(
                Q(username__icontains=termino_busqueda)
                | Q(email__icontains=termino_busqueda)
                | Q(first_name__icontains=termino_busqueda)
                | Q(last_name__icontains=termino_busqueda)
            ).distinct()
        else:
            estudiantes_disponibles = estudiantes_disponibles.none()

        context.update(
            {
                "form_importacion": ImportarEstudiantesExcelForm(),
                "form_colaborador": kwargs.get(
                    "form_colaborador", CursoColaboradorForm(curso=self.object)
                ),
                "docentes_colaboradores": self.object.docentes_colaboradores.select_related(
                    "profile", "profile__position_FK"
                ).order_by("first_name", "last_name", "username"),
                "estudiantes_curso": estudiantes_curso,
                "estudiantes_disponibles": estudiantes_disponibles[:30],
                "termino_busqueda": termino_busqueda,
            }
        )

        return context


class CursoAgregarEstudianteView(PermitsPositionMixin, View):
    def post(self, request, pk, usuario_pk):
        curso = get_object_or_404(objetos_del_docente(Curso.objects.all(), request.user), pk=pk)

        estudiante = get_object_or_404(
            User.objects.select_related("profile", "profile__position_FK"),
            pk=usuario_pk,
            is_active=True,
            profile__position_FK__permission_code="RESTRICTED",
        )

        if curso.estudiantes.filter(pk=estudiante.pk).exists():
            messages.info(request, "Este estudiante ya pertenece al curso.")
        else:
            curso.estudiantes.add(estudiante)
            messages.success(
                request,
                f"{estudiante.get_full_name() or estudiante.username} fue agregado al curso.",
            )

        return redirect("clinitensdocente:curso_detalle", pk=curso.pk)


class CursoQuitarEstudianteView(PermitsPositionMixin, View):
    def post(self, request, pk, usuario_pk):
        curso = get_object_or_404(objetos_del_docente(Curso.objects.all(), request.user), pk=pk)

        estudiante = get_object_or_404(User, pk=usuario_pk)

        curso.estudiantes.remove(estudiante)

        messages.success(
            request,
            f"{estudiante.get_full_name() or estudiante.username} fue quitado del curso.",
        )

        return redirect("clinitensdocente:curso_detalle", pk=curso.pk)


class CursoAgregarColaboradorView(PermitsPositionMixin, View):
    def post(self, request, pk):
        curso = get_object_or_404(
            objetos_del_docente(Curso.objects.all(), request.user), pk=pk
        )
        form = CursoColaboradorForm(request.POST, curso=curso)
        if not form.is_valid():
            messages.error(request, "Selecciona un docente activo disponible para colaborar.")
            return redirect("clinitensdocente:curso_detalle", pk=curso.pk)
        docente = form.cleaned_data["docente"]
        curso.docentes_colaboradores.add(docente)
        messages.success(
            request,
            f"{docente.get_full_name() or docente.username} ahora puede gestionar recetas FarmaTEF de este curso.",
        )
        return redirect("clinitensdocente:curso_detalle", pk=curso.pk)


class CursoQuitarColaboradorView(PermitsPositionMixin, View):
    def post(self, request, pk, usuario_pk):
        curso = get_object_or_404(
            objetos_del_docente(Curso.objects.all(), request.user), pk=pk
        )
        docente = get_object_or_404(
            curso.docentes_colaboradores.all(),
            pk=usuario_pk,
        )
        curso.docentes_colaboradores.remove(docente)
        messages.success(
            request,
            f"Se retiró el acceso de {docente.get_full_name() or docente.username} a las recetas FarmaTEF de este curso.",
        )
        return redirect("clinitensdocente:curso_detalle", pk=curso.pk)


class CursoImportarExcelView(PermitsPositionMixin, View):
    template_name = "pages/clinitens/docente/curso_importacion_resultado.html"

    def post(self, request, pk):
        from .students import leer_filas, importar, guardar_credenciales
        curso = get_object_or_404(objetos_del_docente(Curso.objects.all(), request.user), pk=pk)
        form = ImportarEstudiantesExcelForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, "Selecciona un Excel válido de hasta 5 MB.")
            return redirect("clinitensdocente:curso_detalle", pk=curso.pk)
        try:
            resumen, credenciales = importar(leer_filas(form.cleaned_data["archivo"]), curso,
                normalizar_encabezado, generar_contrasena_temporal)
        except ValidationError as error:
            messages.error(request, "; ".join(error.messages))
            return redirect("clinitensdocente:curso_detalle", pk=curso.pk)
        token = guardar_credenciales(request, curso, credenciales)
        response = render(request, self.template_name, {
            "curso": curso, **resumen, "token_credenciales": token,
            "credenciales": [{k: v for k, v in row.items() if k != "password"} for row in credenciales],
        })
        response["Cache-Control"] = "no-store"
        return response



class CursoCredencialesExcelView(PermitsPositionMixin, View):
    def post(self, request, pk):
        from .students import consumir_credenciales, excel_credenciales
        curso = get_object_or_404(objetos_del_docente(Curso.objects.all(), request.user), pk=pk)
        try:
            rows = consumir_credenciales(request, curso, request.POST.get("token", ""))
        except ValidationError:
            return HttpResponse("Descarga inválida, caducada o ya utilizada.", status=400)
        response = HttpResponse(excel_credenciales(rows), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="credenciales_curso_{curso.pk}.xlsx"'
        response["Cache-Control"] = "no-store"
        return response



class CursoPlantillaExcelView(PermitsPositionMixin, View):
    def get(self, request):
        libro = Workbook()
        hoja = libro.active
        hoja.title = "Estudiantes"

        encabezados = ["username", "email", "first_name", "last_name"]
        hoja.append(encabezados)

        hoja.append(
            [
                "maria.lopez",
                "maria.lopez@inacapmail.cl",
                "María",
                "López",
            ]
        )

        relleno = PatternFill("solid", fgColor="1D4F91")

        for celda in hoja[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = relleno

        hoja.column_dimensions["A"].width = 24
        hoja.column_dimensions["B"].width = 38
        hoja.column_dimensions["C"].width = 24
        hoja.column_dimensions["D"].width = 24

        contenido = BytesIO()
        libro.save(contenido)
        contenido.seek(0)

        respuesta = HttpResponse(
            contenido.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument." "spreadsheetml.sheet"
            ),
        )

        respuesta["Content-Disposition"] = (
            'attachment; filename="plantilla_importacion_estudiantes.xlsx"'
        )

        return respuesta


class CursoDeleteView(PermitsPositionMixin, View):

    def post(self, request, pk, *args, **kwargs):
        curso = get_object_or_404(
            objetos_del_docente(Curso.objects.all(), request.user),
            pk=pk,
        )

        if curso.estudiantes.exists() or curso.actividades.exists():
            messages.error(
                request,
                "No puedes eliminar este curso porque tiene estudiantes inscritos.",
            )
            return redirect("clinitensdocente:curso_detalle", pk=curso.pk)

        nombre_curso = curso.nombre
        curso.delete()

        messages.success(request, f'Curso "{nombre_curso}" eliminado correctamente.')
        return redirect("clinitensdocente:cursos")


class DashboardDocenteView(PermitsPositionMixin, TemplateView):
    template_name = "pages/clinitens/docente/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        fichas = fichas_visibles_para(self.request.user).select_related(
            "estudiante",
            "estudiante__profile__position_FK",
            "codigo_actividad__caso_clinico",
        )

        # No cuenta como estudiante a quien tenga rol Administrador o Docente.
        estudiantes_unicos = (
            fichas.exclude(
                estudiante__profile__position_FK__permission_code__in=[
                    "MANAGER",
                    "ADMIN",
                ]
            )
            .exclude(estudiante__email="")
            .values("estudiante__email")
            .distinct()
            .count()
        )

        fichas_recientes = fichas.filter(
            estado__in=[
                FichaClinica.Estado.ENVIADA,
                FichaClinica.Estado.CALIFICADA,
            ]
        ).order_by("-actualizado_en")[:10]

        context.update(
            {
                "total_casos": objetos_del_docente(CasoClinico.objects.all(), self.request.user).count(),
                "codigos_activos": objetos_del_docente(CodigoActividad.objects.filter(activo=True), self.request.user).count(),
                "total_pacientes": objetos_del_docente(Paciente.objects.all(), self.request.user).count(),
                "total_estudiantes": estudiantes_unicos,
                "fichas_pendientes": fichas.filter(
                    estado=FichaClinica.Estado.ENVIADA
                ).count(),
                "fichas_calificadas": fichas.filter(
                    estado=FichaClinica.Estado.CALIFICADA
                ).count(),
                "fichas_recientes": fichas_recientes,
            }
        )

        return context


class CasoClinicoListCreateView(PermitsPositionMixin, ListView):
    model = CasoClinico
    template_name = "pages/clinitens/docente/casos.html"
    context_object_name = "casos"

    def get_queryset(self):
        return objetos_del_docente(CasoClinico.objects.all(), self.request.user).select_related("creado_por").prefetch_related(
            "archivos",
            "codigos",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", CasoClinicoForm(actor=self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        form = CasoClinicoForm(request.POST, request.FILES, actor=request.user)

        if form.is_valid():
            caso = form.save(commit=False)
            caso.creado_por = request.user
            caso.save()

            for archivo in request.FILES.getlist("archivos"):
                CasoMultimedia.objects.create(caso=caso, archivo=archivo)

            messages.success(request, "Caso clínico creado correctamente.")
            return redirect("clinitensdocente:casos")

        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))


class CasoClinicoUpdateView(FormularioDocenteMixin, PropietarioMixin, PermitsPositionMixin, UpdateView):
    model = CasoClinico
    form_class = CasoClinicoForm
    template_name = "pages/clinitens/docente/formulario.html"
    success_url = reverse_lazy("clinitensdocente:casos")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        for archivo in self.request.FILES.getlist("archivos"):
            CasoMultimedia.objects.create(caso=self.object, archivo=archivo)
        messages.success(self.request, "Caso clínico actualizado.")
        return respuesta


class CasoClinicoDeleteView(PropietarioMixin, PermitsPositionMixin, DeleteView):
    model = CasoClinico
    success_url = reverse_lazy("clinitensdocente:casos")

    def post(self, request, *args, **kwargs):
        try:
            messages.success(request, "Caso clínico eliminado correctamente.")
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar este caso porque tiene códigos de actividad asociados.",
            )
            return redirect("clinitensdocente:casos")


class CasoClinicoPreviewView(PermitsPositionMixin, DetailView):
    model = CasoClinico
    template_name = "pages/clinitens/docente/caso_previsualizar.html"
    context_object_name = "caso"

    def get_queryset(self):
        return objetos_del_docente(CasoClinico.objects.all(), self.request.user).prefetch_related("archivos", "codigos")


class CodigoListCreateView(PermitsPositionMixin, ListView):
    model = CodigoActividad
    template_name = "pages/clinitens/docente/codigos.html"
    context_object_name = "codigos"

    def get_queryset(self):
        return objetos_del_docente(CodigoActividad.objects.all(), self.request.user).select_related("caso_clinico").annotate(
            total_estudiantes=Count("fichas_estudiantes__estudiante", distinct=True),
            en_linea=Count("fichas_estudiantes__estudiante", filter=Q(
                fichas_estudiantes__estudiante__profile__last_activity__gte=timezone.now()-timezone.timedelta(minutes=10)), distinct=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", CodigoActividadForm(actor=self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        form = CodigoActividadForm(request.POST, actor=request.user)
        if form.is_valid():
            codigo = form.save(commit=False)
            codigo.creado_por = codigo.curso.creado_por if codigo.curso_id else codigo.caso_clinico.creado_por
            codigo.save()
            messages.success(request, "Código de actividad creado.")
            return redirect("clinitensdocente:codigos")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))


class CodigoActividadToggleView(PermitsPositionMixin, View):

    def post(self, request, pk, *args, **kwargs):
        codigo = get_object_or_404(objetos_del_docente(CodigoActividad.objects.all(), request.user), pk=pk)

        codigo.activo = not codigo.activo
        codigo.save(update_fields=["activo"])

        estado = "activado" if codigo.activo else "desactivado"

        messages.success(
            request, f'El código "{codigo.codigo}" fue {estado} correctamente.'
        )

        return redirect("clinitensdocente:codigos")


class PacienteListCreateView(PermitsPositionMixin, ListView):
    model = Paciente
    template_name = "pages/clinitens/docente/pacientes.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        return objetos_del_docente(Paciente.objects.all(), self.request.user).prefetch_related("resultados")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", PacienteForm(actor=self.request.user))
        return context

    def post(self, request, *args, **kwargs):
        form = PacienteForm(request.POST, request.FILES, actor=request.user)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.creado_por = request.user
            paciente.save()
            for archivo in request.FILES.getlist("archivos"):
                PacienteMultimedia.objects.create(paciente=paciente, archivo=archivo)
            messages.success(request, "Paciente registrado correctamente.")
            return redirect("clinitensdocente:pacientes")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))


class PacienteUpdateView(FormularioDocenteMixin, PropietarioMixin, PermitsPositionMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "pages/clinitens/docente/formulario.html"
    success_url = reverse_lazy("clinitensdocente:pacientes")

    def form_valid(self, form):
        respuesta = super().form_valid(form)
        for archivo in self.request.FILES.getlist("archivos"):
            PacienteMultimedia.objects.create(paciente=self.object, archivo=archivo)
        messages.success(self.request, "Paciente actualizado.")
        return respuesta


class PacienteDeleteView(PropietarioMixin, PermitsPositionMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy("clinitensdocente:pacientes")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Paciente eliminado.")
        return super().post(request, *args, **kwargs)


class PacienteDetalleView(PermitsPositionMixin, View):

    def get(self, request, pk, *args, **kwargs):
        paciente = get_object_or_404(objetos_del_docente(Paciente.objects.all(), request.user), pk=pk)

        diagnosticos = [
            diagnostico
            for diagnostico in [
                paciente.diagnostico_1,
                paciente.diagnostico_2,
            ]
            if diagnostico
        ]

        return JsonResponse(
            {
                "id": paciente.pk,
                "rut": paciente.rut,
                "nombre": paciente.nombre_completo,
                "edad": paciente.edad,
                "sexo": paciente.get_sexo_display(),
                "comuna": paciente.ciudad_comuna or "Sin información",
                "cesfam": paciente.centro_atencion or "Sin información",
                "diagnosticos": diagnosticos,
                "observaciones": paciente.observaciones
                or "Sin observaciones registradas.",
                "historial": [],
            }
        )


class ResultadoListCreateView(PermitsPositionMixin, ListView):
    model = ResultadoDiagnostico
    template_name = "pages/clinitens/docente/apoyo_diagnostico.html"
    context_object_name = "resultados"

    def get_queryset(self):
        return objetos_del_docente(ResultadoDiagnostico.objects.all(), self.request.user).select_related("paciente", "caso_clinico")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get(
            "form",
            ResultadoDiagnosticoForm(
                actor=self.request.user, initial={
                    "fecha": timezone.localdate(),
                    "hora": timezone.localtime()
                    .time()
                    .replace(second=0, microsecond=0),
                }
            ),
        )
        return context

    def post(self, request, *args, **kwargs):
        form = ResultadoDiagnosticoForm(request.POST, request.FILES, actor=request.user)
        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.creado_por = resultado.paciente.creado_por
            resultado.save()
            messages.success(request, "Resultado asociado correctamente.")
            return redirect("clinitensdocente:apoyo_diagnostico")
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))


class ResultadoHabilitarView(PermitsPositionMixin, View):
    def post(self, request, pk):
        resultado = get_object_or_404(objetos_del_docente(ResultadoDiagnostico.objects.all(), request.user), pk=pk)
        if resultado.publicacion != ResultadoDiagnostico.Publicacion.HABILITACION_DOCENTE:
            return HttpResponse("Este resultado no requiere habilitación.", status=400)
        ResultadoDiagnostico.objects.filter(pk=pk).update(habilitado=not resultado.habilitado)
        messages.success(request, "Disponibilidad del resultado actualizada.")
        return redirect("clinitensdocente:apoyo_diagnostico")


class ResultadoDeleteView(PropietarioMixin, PermitsPositionMixin, DeleteView):
    model = ResultadoDiagnostico
    success_url = reverse_lazy("clinitensdocente:apoyo_diagnostico")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Resultado eliminado.")
        return super().post(request, *args, **kwargs)


class EstudiantesListView(PermitsPositionMixin, ListView):
    model = FichaClinica
    template_name = "pages/clinitens/docente/estudiantes.html"
    context_object_name = "fichas"

    def get_queryset(self):
        queryset = (
            fichas_visibles_para(self.request.user).filter(
                estado__in=[
                    FichaClinica.Estado.ENVIADA,
                    FichaClinica.Estado.CALIFICADA,
                ],
            )
            .select_related(
                "estudiante",
                "codigo_actividad",
                "codigo_actividad__caso_clinico",
            )
            .order_by("-enviada_en")
        )

        curso_id = self.request.GET.get("curso")

        if curso_id:
            if not curso_id.isdigit():
                raise Http404("Curso no válido.")
            curso = get_object_or_404(
                objetos_del_docente(Curso.objects.all(), self.request.user),
                pk=curso_id,
            )

            queryset = queryset.filter(
                estudiante__in=curso.estudiantes.all()
            ).distinct()

        busqueda = self.request.GET.get("q", "").strip()

        if busqueda:
            queryset = queryset.filter(
                Q(codigo_actividad__codigo__icontains=busqueda)
                | Q(codigo_actividad__caso_clinico__titulo__icontains=busqueda)
                | Q(estudiante__username__icontains=busqueda)
                | Q(estudiante__email__icontains=busqueda)
                | Q(estudiante__first_name__icontains=busqueda)
                | Q(estudiante__last_name__icontains=busqueda)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        curso_id = self.request.GET.get("curso")

        context["cursos"] = objetos_del_docente(Curso.objects.all(), self.request.user).order_by(
            "nombre"
        )

        context["curso_seleccionado"] = (
            context["cursos"].filter(pk=curso_id).first() if curso_id else None
        )

        context["busqueda"] = self.request.GET.get("q", "").strip()

        return context


class FichaRubricaView(PermitsPositionMixin, TemplateView):
    template_name = "pages/clinitens/docente/rubrica.html"

    def get_ficha(self):
        ficha = (
            fichas_visibles_para(self.request.user).select_related(
                "estudiante",
                "codigo_actividad",
                "codigo_actividad__caso_clinico",
            )
            .filter(
                pk=self.kwargs["pk"],
                estado__in=[
                    FichaClinica.Estado.ENVIADA,
                    FichaClinica.Estado.CALIFICADA,
                ],
            )
            .first()
        )

        if not ficha:
            raise Http404("Ficha no encontrada.")

        return ficha

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ficha = self.get_ficha()

        criterios = []
        for codigo, indicador, maximo in RUBRICA:
            criterios.append(
                {
                    "codigo": codigo,
                    "indicador": indicador,
                    "maximo": maximo,
                    "niveles": niveles_por_puntaje(maximo),
                }
            )

        seleccionados = ficha.evaluacion_rubrica.get("puntajes", {})

        modo_edicion = (
            ficha.estado != FichaClinica.Estado.CALIFICADA
            or self.request.GET.get("editar") == "1"
        )

        if modo_edicion and ficha.borrador_evaluacion:
            seleccionados = ficha.borrador_evaluacion.get("puntajes", {})
        context.update(
            {
                "retroalimentacion_editor": ficha.borrador_evaluacion.get("retroalimentacion", ficha.retroalimentacion) if modo_edicion else ficha.retroalimentacion,
                "ficha": ficha,
                "criterios": criterios,
                "puntaje_maximo": sum(item[2] for item in RUBRICA),
                "seleccionados": seleccionados,
                "modo_edicion": modo_edicion,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        from .evaluation import guardar_evaluacion
        ficha = self.get_ficha()
        if ficha.estado == FichaClinica.Estado.CALIFICADA and request.POST.get("modo_edicion") != "1":
            return HttpResponse("Activa Editar evaluación antes de modificarla.", status=400)
        try:
            raw = request.POST.get("puntajes_json", "{}")
            if len(raw) > 10_000:
                raise ValidationError("Evaluación demasiado extensa.")
            puntajes = json.loads(raw)
            version = int(request.POST["version"])
            updated = guardar_evaluacion(ficha, request.user, puntajes,
                request.POST.get("retroalimentacion", "").strip(),
                request.POST.get("accion", "guardar"), version)
        except (json.JSONDecodeError, ValueError, KeyError, ValidationError) as error:
            return HttpResponse(str(error), status=400, content_type="text/plain; charset=utf-8")
        if not updated:
            return HttpResponse("La evaluación cambió. Vuelve a abrirla antes de guardar.", status=409)
        messages.success(request, "Evaluación publicada." if request.POST.get("accion") == "publicar"
                         else "Borrador guardado. La publicación anterior se conserva.")
        return redirect("clinitensdocente:ficha_rubrica", pk=ficha.pk)


class FichaEstudianteRevisionView(PermitsPositionMixin, TemplateView):
    template_name = "pages/clinitens/ficha/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ficha = (
            fichas_visibles_para(self.request.user).select_related(
                "estudiante",
                "codigo_actividad",
                "codigo_actividad__caso_clinico",
            )
            .filter(pk=self.kwargs["pk"])
            .first()
        )

        if not ficha:
            raise Http404("Ficha no encontrada.")

        clave = self.kwargs.get("seccion", "identidad")
        secciones_dict = {item[0]: item for item in SECCIONES}

        if clave not in secciones_dict:
            raise Http404("Sección no encontrada.")

        context.update(
            {
                "ficha": ficha,
                "secciones": SECCIONES,
                "seccion_actual": clave,
                "titulo_seccion": secciones_dict[clave][2],
                "datos_json": json.dumps(ficha.datos or {}),
                "henderson": HENDERSON,
                "maslow": MASLOW,
                "glasgow": GCS,
                "downton": DOWNTON,
                "braden": BRADEN,
                "aislamientos": [
                    "Precauciones estándar",
                    "Contacto",
                    "Gotas",
                    "Aéreo",
                ],
                "epp": [
                    "Mascarilla quirúrgica",
                    "Mascarilla N95",
                    "Pechera",
                    "Guantes",
                    "Antiparras / escudo facial",
                    "Cofia",
                    "Botas",
                ],
                "habitaciones": [
                    "Individual",
                    "Compartida",
                    "Aislamiento",
                    "UCI / UTI",
                ],
                "base_template": "pages/clinitens/docente/base_revision_ficha.html",
                "ruta_editor": "clinitensdocente:ficha_revisar",
                "modo_revision": True,
                "desde_en_vivo": self.request.GET.get("origen") == "en_vivo",
                "mostrar_acciones_evaluacion": (
                    self.request.GET.get("origen") != "en_vivo"
                    and ficha.estado
                    in [
                        FichaClinica.Estado.ENVIADA,
                        FichaClinica.Estado.CALIFICADA,
                    ]
                ),
                "parametros_origen": self.request.GET.urlencode(),
            }
        )

        return context


@login_required
@require_GET
def exportar_ficha_pdf(request, pk):
    if not es_docente(request.user):
        raise PermissionDenied("La exportación requiere permiso docente.")
    ficha = (
        fichas_visibles_para(request.user)
        .filter(
            pk=pk,
            estado__in=[
                FichaClinica.Estado.ENVIADA,
                FichaClinica.Estado.CALIFICADA,
            ],
        )
        .first()
    )

    if not ficha:
        raise Http404("Ficha no encontrada.")

    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Spacer,
        Paragraph,
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="ficha_{ficha.pk}_{ficha.estudiante.username}.pdf"'
    )

    documento = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    estilos = getSampleStyleSheet()
    titulo = estilos["Title"]
    encabezado = estilos["Heading2"]
    normal = estilos["BodyText"]

    encabezado.textColor = HexColor("#1d65b7")
    encabezado.keepWithNext = True

    historia = [
        Paragraph("CliniTENS · Ficha Clínica", titulo),
        Spacer(1, 10),
        Paragraph(
            f"<b>Estudiante:</b> {escape(ficha.estudiante.get_full_name() or ficha.estudiante.username)}",
            normal,
        ),
        Paragraph(f"<b>Correo:</b> {escape(ficha.estudiante.email)}", normal),
        Paragraph(
            f"<b>Código:</b> {escape(ficha.codigo_actividad.codigo)}",
            normal,
        ),
        Paragraph(
            f"<b>Caso clínico:</b> {escape(ficha.codigo_actividad.caso_clinico.titulo)}",
            normal,
        ),
        Paragraph(
            f"<b>Estado:</b> {escape(ficha.get_estado_display())}",
            normal,
        ),
        Spacer(1, 14),
    ]

    for seccion in preparar_secciones_ficha(ficha.datos):
        historia.append(Paragraph(escape(seccion["titulo"]), encabezado))

        for etiqueta, valor in seccion["filas"]:
            historia.append(
                Paragraph(
                    f"<b>{escape(etiqueta)}:</b> {escape(valor)}",
                    normal,
                )
            )

        historia.append(Spacer(1, 10))

    documento.build(historia)
    return response


class EnVivoView(PermitsPositionMixin, TemplateView):
    template_name = "pages/clinitens/docente/en_vivo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cursos = objetos_del_docente(Curso.objects.all(), self.request.user).order_by("nombre")

        codigos = (
            objetos_del_docente(CodigoActividad.objects.filter(activo=True), self.request.user)
            .select_related("caso_clinico")
            .order_by("codigo")
        )

        curso_id = self.request.GET.get("curso", "").strip()
        if curso_id and not curso_id.isdigit():
            raise Http404("Curso no válido.")
        codigo_id = self.request.GET.get("codigo", "").strip()
        if codigo_id and not codigo_id.isdigit():
            raise Http404("Código no válido.")
        limite_inactividad = timezone.now() - timezone.timedelta(minutes=10)

        curso_seleccionado = cursos.filter(pk=curso_id).first() if curso_id else None

        codigo_seleccionado = (
            codigos.filter(pk=codigo_id).first() if codigo_id else None
        )

        registros = []

        # El código es obligatorio para calcular el avance.
        if codigo_seleccionado:

            if curso_seleccionado:
                # Solo estudiantes del curso seleccionado.
                estudiantes = (
                    curso_seleccionado.estudiantes.filter(is_active=True)
                    .select_related("profile", "profile__position_FK")
                    .order_by("first_name", "last_name", "username")
                )

            else:
                # Sin curso: solo estudiantes vinculados al docente.
                estudiantes = (
                    User.objects.filter(
                        is_active=True,
                        profile__position_FK__permission_code__iexact="RESTRICTED",
                    )
                    .filter(Q(cursos_clinitens__in=cursos) | Q(fichas_clinicas__codigo_actividad=codigo_seleccionado))
                    .distinct()
                    .select_related("profile", "profile__position_FK")
                    .order_by("first_name", "last_name", "username")
                )

            fichas = (
                fichas_visibles_para(self.request.user).filter(
                    estudiante__in=estudiantes,
                    codigo_actividad=codigo_seleccionado,
                )
                .select_related("estudiante")
                .order_by("-actualizado_en")
            )

            fichas_por_estudiante = {}

            for ficha in fichas:
                if ficha.estudiante_id not in fichas_por_estudiante:
                    fichas_por_estudiante[ficha.estudiante_id] = ficha

            for estudiante in estudiantes:
                ficha = fichas_por_estudiante.get(estudiante.pk)

                if not ficha:
                    estado = "SIN_INICIAR"
                    completadas = 0

                else:
                    datos = ficha.datos or {}

                    completadas = sum(
                        1
                        for clave in SECCIONES_FICHA
                        if seccion_completa(clave, datos.get(clave, {}))
                    )

                    ultima_actividad = None

                    try:
                        ultima_actividad = estudiante.profile.last_activity
                    except Profile.DoesNotExist:
                        pass

                    if ficha.estado in [
                        FichaClinica.Estado.ENVIADA,
                        FichaClinica.Estado.CALIFICADA,
                    ]:
                        estado = "FINALIZADO"

                    elif completadas == 0:
                        estado = "SIN_INICIAR"

                    elif ultima_actividad and ultima_actividad >= limite_inactividad:
                        estado = "EN_PROCESO"

                    else:
                        estado = "INACTIVO"

                registros.append(
                    {
                        "estudiante": estudiante,
                        "ficha": ficha,
                        "estado": estado,
                        "completadas": completadas,
                        "total_secciones": len(SECCIONES_FICHA),
                    }
                )

        context.update(
            {
                "cursos": cursos,
                "codigos": codigos,
                "curso_seleccionado": curso_seleccionado,
                "codigo_seleccionado": codigo_seleccionado,
                "registros": registros,
                "total": len(registros),
                "finalizados": sum(
                    1 for item in registros if item["estado"] == "FINALIZADO"
                ),
                "en_proceso": sum(
                    1 for item in registros if item["estado"] == "EN_PROCESO"
                ),
                "inactivos": sum(
                    1 for item in registros if item["estado"] == "INACTIVO"
                ),
                "sin_iniciar": sum(
                    1 for item in registros if item["estado"] == "SIN_INICIAR"
                ),
            }
        )

        return context
