from django.contrib import admin
from .models import Profile, Position
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.unregister(User)


@admin.register(User)
class UsuarioProtegidoAdmin(UserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return obj is None or not obj.is_superuser or obj.pk == request.user.pk

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or not obj.is_superuser)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user_FK",)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or not obj.user_FK.is_superuser or obj.user_FK_id == request.user.pk)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or not obj.user_FK.is_superuser)


admin.site.register(Profile, ProfileAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ("user_position",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or not obj.profile_set.filter(user_FK__is_superuser=True).exclude(user_FK=request.user).exists())

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and (obj is None or not obj.profile_set.filter(user_FK__is_superuser=True).exists())


admin.site.register(Position, PositionAdmin)
