from unicodedata import combining, normalize

from core.permissions import objetos_del_docente
from .models import Medicamento


TIPOS_ALERTA = {
    "stock-bajo": ("Stock bajo", "stock_bajo"),
    "vencimiento": ("Vencimiento próximo", "proximo_a_vencer"),
}


def inventario_visible(usuario):
    return objetos_del_docente(Medicamento.objects.all(), usuario)


def resumen_alertas(usuario):
    medicamentos = list(inventario_visible(usuario).filter(activo=True).prefetch_related("lotes"))
    return [
        {
            "tipo": tipo,
            "titulo": titulo,
            "total": sum(getattr(medicamento, campo) for medicamento in medicamentos),
        }
        for tipo, (titulo, campo) in TIPOS_ALERTA.items()
    ]


def _texto_busqueda(texto):
    return "".join(letra for letra in normalize("NFD", texto.casefold()) if not combining(letra))


def filtrar_inventario(medicamentos, busqueda, alerta):
    campo_alerta = TIPOS_ALERTA.get(alerta, ("", None))[1]
    terminos = _texto_busqueda(busqueda).split()

    for medicamento in medicamentos:
        if campo_alerta and not getattr(medicamento, campo_alerta):
            continue
        if terminos:
            texto = _texto_busqueda(" ".join([
                medicamento.nombre,
                medicamento.clasificacion,
                medicamento.principio_activo,
                medicamento.concentracion,
                medicamento.forma_farmaceutica,
                *(lote.numero_lote for lote in medicamento.lotes.all()),
            ]))
            if not all(termino in texto for termino in terminos):
                continue
        yield medicamento
