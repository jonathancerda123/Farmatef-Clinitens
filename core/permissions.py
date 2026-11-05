"""Permisos compartidos; nunca dependen del ID de un cargo."""
from django.db.models import Q


def cargo(usuario):
    if not usuario.is_authenticated or not usuario.is_active:
        return None
    perfil = getattr(usuario, "profile", None)
    return getattr(getattr(perfil, "position_FK", None), "permission_code", None)


def es_administrador(usuario):
    return bool(usuario.is_authenticated and usuario.is_active and
                (usuario.is_superuser or cargo(usuario) == "ADMIN"))


def es_docente(usuario):
    return es_administrador(usuario) or cargo(usuario) == "MANAGER"


def objetos_del_docente(queryset, usuario, campo="creado_por"):
    if es_administrador(usuario):
        return queryset
    if cargo(usuario) == "MANAGER":
        return queryset.filter(**{campo: usuario})
    return queryset.none()


def cursos_visibles_para_docente(queryset, usuario):
    """Cursos propios o compartidos explícitamente con un docente activo."""
    if es_administrador(usuario):
        return queryset
    if cargo(usuario) == "MANAGER":
        return queryset.filter(
            Q(creado_por=usuario) | Q(docentes_colaboradores=usuario)
        ).distinct()
    return queryset.none()


def recetas_visibles_para_docente(queryset, usuario):
    """Recetas propias sin curso y recetas vinculadas a cursos propios/compartidos."""
    if es_administrador(usuario):
        return queryset
    if cargo(usuario) == "MANAGER":
        return queryset.filter(
            Q(curso__isnull=True, creado_por=usuario)
            | Q(curso__creado_por=usuario)
            | Q(curso__docentes_colaboradores=usuario)
        ).distinct()
    return queryset.none()
