import json
from datetime import date, timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from FarmaTEFApp.models import LoteInventario, Medicamento


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
ARSENAL_PATH = DATA_DIR / "arsenal_aps_2024_2026.json"
LEGACY_PATH = DATA_DIR / "vademecum_2023_nombres.json"
FUENTE = "Arsenal Farmacoterapéutico APS 2024–2026"
LOTE_PREFIX = "SIM-APS-2024-2026-"


def presentation_name(item):
    return f"{item['nombre'].title()} - {item['concentracion']} - {item['forma'].title()}"


class Command(BaseCommand):
    help = "Prepara o reemplaza el catálogo FarmaTEF con el arsenal APS 2024–2026."

    def add_arguments(self, parser):
        parser.add_argument("--responsable", required=True, help="Usuario propietario del catálogo, por ejemplo valita.")
        parser.add_argument("--apply", action="store_true", help="Aplica el reemplazo. Sin esta opción solo muestra el resumen.")

    def handle(self, *args, **options):
        arsenal = json.loads(ARSENAL_PATH.read_text(encoding="utf-8"))
        legacy_names = json.loads(LEGACY_PATH.read_text(encoding="utf-8"))
        names = [presentation_name(item) for item in arsenal]
        if len(arsenal) != 363 or len(set(names)) != len(names):
            raise CommandError("El archivo fuente debe contener 363 presentaciones con nombres únicos.")
        if max(map(len, names)) > 160:
            raise CommandError("Hay nombres de presentación que exceden el límite del modelo.")

        User = get_user_model()
        try:
            owner = User.objects.get(username=options["responsable"], is_active=True)
        except User.DoesNotExist as exc:
            raise CommandError("No existe una cuenta activa con ese nombre de usuario.") from exc
        old = Medicamento.objects.filter(creado_por=owner, nombre__in=legacy_names)
        old_count = old.count()
        existing_new = Medicamento.objects.filter(creado_por=owner, fuente_documental=FUENTE).count()
        if old_count not in (0, 109):
            raise CommandError(f"Se esperaban 109 registros antiguos o ninguno; se encontraron {old_count}. No se modificó nada.")
        if existing_new:
            raise CommandError(f"Ya existen {existing_new} registros de esta fuente para {owner.username}; no se modificó nada.")

        self.stdout.write(f"Responsable: {owner.username}")
        self.stdout.write(f"Registros antiguos que se archivarán: {old_count}")
        self.stdout.write(f"Presentaciones nuevas: {len(arsenal)}")
        self.stdout.write("Lotes ficticios a crear: 363; unidades: 1–40 por lote; vencimientos: 20–719 días desde la carga.")
        self.stdout.write("Sin --apply no se escribió ningún dato.")
        if not options["apply"]:
            return

        today = date.today()
        with transaction.atomic():
            old.update(activo=False)
            new_medicines = []
            for item in arsenal:
                new_medicines.append(Medicamento(
                    nombre=presentation_name(item),
                    principio_activo=item["nombre"],
                    concentracion=item["concentracion"],
                    forma_farmaceutica=item["forma"],
                    clasificacion=item["clasificacion"],
                    observaciones=item["observaciones"],
                    fuente_documental=FUENTE,
                    stock_minimo=10,
                    dias_alerta_vencimiento=90,
                    activo=True,
                    creado_por=owner,
                ))
            Medicamento.objects.bulk_create(new_medicines)
            new_medicines = list(Medicamento.objects.filter(creado_por=owner, fuente_documental=FUENTE).order_by("id"))
            lots = []
            for index, medicine in enumerate(new_medicines, start=1):
                lots.append(LoteInventario(
                    medicamento=medicine,
                    numero_lote=f"{LOTE_PREFIX}{index:03d}",
                    vence_el=today + timedelta(days=20 + ((index - 1) * 97) % 700),
                    unidades=((index - 1) * 17) % 40 + 1,
                    registrado_por=owner,
                    es_simulado=True,
                ))
            LoteInventario.objects.bulk_create(lots)
        self.stdout.write(self.style.SUCCESS("Reemplazo aplicado: 109 registros antiguos archivados y 363 presentaciones/lotes simulados cargados."))
