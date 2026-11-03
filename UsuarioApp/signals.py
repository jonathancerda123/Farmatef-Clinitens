from django.dispatch import receiver
from allauth.account.signals import password_changed, password_set, password_reset
from .models import Profile


@receiver(password_changed)
@receiver(password_set)
@receiver(password_reset)
def password_actualizado(request, user, **kwargs):
    Profile.objects.filter(user_FK=user).update(
        requiere_cambio_password=False, password_temporal_expira=None)
