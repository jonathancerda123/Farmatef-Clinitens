from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class CambioPasswordObligatorioMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, "profile", None)
            if profile and profile.requiere_cambio_password:
                allowed = {reverse("account_change_password"), reverse("account_logout")}
                if profile.password_temporal_expira and profile.password_temporal_expira <= timezone.now():
                    logout(request)
                    return redirect("account_reset_password")
                if request.path not in allowed and not request.path.startswith("/static/"):
                    return redirect("account_change_password")
        return self.get_response(request)
