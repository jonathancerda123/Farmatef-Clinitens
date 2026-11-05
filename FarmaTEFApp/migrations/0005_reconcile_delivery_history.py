from django.db import migrations
from django.db.models import Sum


def reconcile_delivery_totals(apps, schema_editor):
    Receta = apps.get_model("FarmaTEFApp", "Receta")
    RecetaLinea = apps.get_model("FarmaTEFApp", "RecetaLinea")
    DispensacionLote = apps.get_model("FarmaTEFApp", "DispensacionLote")

    database = schema_editor.connection.alias
    totals = {
        row["linea_id"]: row["total"]
        for row in DispensacionLote.objects.using(database).values("linea_id").annotate(total=Sum("unidades"))
    }
    for linea in RecetaLinea.objects.using(database).all().iterator():
        delivered = totals.get(linea.pk, 0)
        if delivered > linea.unidades:
            raise RuntimeError(
                f"Dispensed quantity exceeds prescribed quantity for recipe line {linea.pk}."
            )
        if linea.unidades_entregadas != delivered:
            RecetaLinea.objects.using(database).filter(pk=linea.pk).update(
                unidades_entregadas=delivered
            )

    for receta in Receta.objects.using(database).all().iterator():
        lineas = list(RecetaLinea.objects.using(database).filter(receta_id=receta.pk))
        if not lineas:
            continue
        if all(linea.unidades_entregadas == linea.unidades for linea in lineas):
            estado = "ENTREGADA"
        elif any(linea.unidades_entregadas for linea in lineas):
            estado = "PARCIAL"
        else:
            continue
        if receta.estado != estado:
            Receta.objects.using(database).filter(pk=receta.pk).update(estado=estado)


class Migration(migrations.Migration):
    dependencies = [
        ("FarmaTEFApp", "0004_receta_es_ficticia_recetalinea_unidades_entregadas_and_more"),
    ]

    operations = [migrations.RunPython(reconcile_delivery_totals, migrations.RunPython.noop)]
