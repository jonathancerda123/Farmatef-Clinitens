from io import BytesIO
from xml.sax.saxutils import escape

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def comprobante_dispensacion(dispensacion):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm, title="Comprobante de dispensación simulada",
    )
    styles = getSampleStyleSheet()
    styles["Title"].textColor = colors.HexColor("#17474E")

    def body(value):
        return Paragraph(escape(str(value)), styles["BodyText"])

    receta = dispensacion.receta
    fecha = timezone.localtime(dispensacion.entregado_en).strftime("%d/%m/%Y %H:%M")
    rows = [[body(value) for value in ("Medicamento", "Lote", "Vencimiento", "Unidades")]]
    for uso in dispensacion.lotes_usados.all():
        medicamento = uso.linea.medicamento
        producto = " · ".join(filter(None, (
            medicamento.nombre, medicamento.concentracion, medicamento.forma_farmaceutica,
        )))
        rows.append([
            body(producto), body(uso.lote.numero_lote),
            body(uso.lote.vence_el.strftime("%d/%m/%Y")), body(uso.unidades),
        ])
    table = Table(rows, colWidths=[72 * mm, 39 * mm, 30 * mm, 22 * mm], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D4EBE7")),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBDDE0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    document.build([
        body("FarmaTEF · Simulación educativa"),
        Paragraph("Comprobante de dispensación simulada", styles["Title"]),
        Spacer(1, 3 * mm),
        body(f"Receta: {receta.numero}"),
        body(f"Fecha de entrega: {fecha}"),
        body(f"Paciente ficticio: {receta.persona_ficticia}"),
        Spacer(1, 6 * mm),
        table,
    ])
    buffer.seek(0)
    return buffer
