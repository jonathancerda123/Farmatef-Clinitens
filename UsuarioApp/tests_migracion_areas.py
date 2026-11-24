"""Ensayo reversible de la migración 034 sobre la base ficticia de pruebas."""
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class MigracionAreasTests(TransactionTestCase):
    def test_docentes_previos_reciben_ambos_y_se_conservan_perfiles(self):
        anterior = [("UsuarioApp", "0003_profile_password_temporal_expira")]
        actual = [("UsuarioApp", "0004_profile_area_docente_and_more")]
        executor = MigrationExecutor(connection)
        executor.migrate(anterior)
        try:
            apps = executor.loader.project_state(anterior).apps
            User = apps.get_model("auth", "User")
            Position = apps.get_model("UsuarioApp", "Position")
            Profile = apps.get_model("UsuarioApp", "Profile")
            ids = {}
            for role in ["MANAGER", "ADMIN", "RESTRICTED"]:
                user = User.objects.create(username=f"previo-{role}")
                position = Position.objects.create(user_position=role, permission_code=role)
                profile = Profile.objects.create(user_FK=user, position_FK=position, requiere_cambio_password=True)
                ids[role] = profile.pk
            sin_cargo = Profile.objects.create(user_FK=User.objects.create(username="previo-sin-cargo"))
            executor = MigrationExecutor(connection)
            executor.migrate(actual)
            Profile = executor.loader.project_state(actual).apps.get_model("UsuarioApp", "Profile")
            for role, pk in ids.items():
                profile = Profile.objects.get(pk=pk)
                self.assertEqual(profile.area_docente, "AMBOS" if role == "MANAGER" else "")
                self.assertTrue(profile.requiere_cambio_password)
            self.assertEqual(Profile.objects.get(pk=sin_cargo.pk).area_docente, "")
            executor = MigrationExecutor(connection)
            executor.migrate(anterior)
            Profile = executor.loader.project_state(anterior).apps.get_model("UsuarioApp", "Profile")
            self.assertEqual(Profile.objects.count(), 4)
        finally:
            MigrationExecutor(connection).migrate(actual)
