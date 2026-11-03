from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.media import archivo_privado, upload_editor_desactivado

urlpatterns = [
    path("media/<path:nombre>", archivo_privado, name="archivo_privado"),
    path("ckeditor5/image_upload/", upload_editor_desactivado, name="ck_editor_5_upload_file"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("homeApp.urls")),
    path("", include("UsuarioApp.urls")),
    path(
        "clinitensdocente/",
        include("CliniTensDocenteApp.urls", namespace="clinitensdocente"),
    ),
    path(
        "ficha-clinica/",
        include("CliniTensFichaApp.urls", namespace="clinitensficha"),
    ),
    path("farmatef/", include("FarmaTEFApp.urls", namespace="farmatef")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
