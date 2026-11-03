"""Fixtures sintéticas compartidas por las pruebas; sin datos del repositorio."""
from django.contrib.auth.models import User
from UsuarioApp.models import Profile, Position


def usuario(nombre, cargo="RESTRICTED", **kwargs):
    user = User.objects.create_user(nombre, email=f"{nombre}@example.test",
                                    password="Clave-ficticia-789", **kwargs)
    if cargo is not None:
        position, _ = Position.objects.get_or_create(
            user_position=cargo, defaults={"permission_code": cargo})
        Profile.objects.create(user_FK=user, position_FK=position)
    return user
