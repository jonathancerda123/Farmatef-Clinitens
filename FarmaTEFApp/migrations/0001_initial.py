# Initial schema authored from FarmaTEFApp models; automatic generation is pending.
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Medicamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=160)),
                ("principio_activo", models.CharField(blank=True, max_length=160)),
                ("concentracion", models.CharField(blank=True, max_length=80)),
                ("forma_farmaceutica", models.CharField(blank=True, max_length=100)),
                ("codigo_barras", models.CharField(blank=True, max_length=64)),
                ("stock_minimo", models.PositiveIntegerField(default=0)),
                ("dias_alerta_vencimiento", models.PositiveSmallIntegerField(default=90, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)])),
                ("activo", models.BooleanField(default=True)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("creado_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="medicamentos_farmatef", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Medicamento",
                "verbose_name_plural": "Medicamentos",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="LoteInventario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_lote", models.CharField(max_length=80)),
                ("vence_el", models.DateField()),
                ("unidades", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("medicamento", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lotes", to="FarmaTEFApp.medicamento")),
                ("registrado_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lotes_farmatef_registrados", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Lote de inventario",
                "verbose_name_plural": "Lotes de inventario",
                "ordering": ["vence_el", "numero_lote"],
            },
        ),
        migrations.AddConstraint(
            model_name="medicamento",
            constraint=models.UniqueConstraint(fields=("creado_por", "nombre"), name="ft_med_autor_nombre_uq"),
        ),
        migrations.AddConstraint(
            model_name="medicamento",
            constraint=models.UniqueConstraint(condition=models.Q(("codigo_barras", ""), _negated=True), fields=("creado_por", "codigo_barras"), name="ft_med_autor_barcode_uq"),
        ),
        migrations.AddConstraint(
            model_name="loteinventario",
            constraint=models.UniqueConstraint(fields=("medicamento", "numero_lote"), name="ft_lote_med_numero_uq"),
        ),
        migrations.AddConstraint(
            model_name="loteinventario",
            constraint=models.CheckConstraint(condition=models.Q(("unidades__gt", 0)), name="ft_lote_unidades_gt0"),
        ),
    ]
