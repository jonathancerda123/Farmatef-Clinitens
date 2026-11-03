from django.db import models, transaction
from .choices import PERMISOS

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import os
from utils.customer_img import resize_image, crop_image


def profile_picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    return f"users/{instance.user_FK.username}/{random_filename}{extension}"


# Create your models here.
class Position(models.Model):
    user_position = models.CharField(max_length=45, unique=True)
    permission_code = models.CharField(
        max_length=25, choices=PERMISOS, default="RESTRICTED"
    )

    class Meta:
        db_table = "position"

    def __str__(self):
        return f"{self.user_position}"


class Profile(models.Model):
    last_activity = models.DateTimeField(null=True, blank=True)
    requiere_cambio_password = models.BooleanField(default=False)
    password_temporal_expira = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=profile_picture_path, default="profile.webp")
    user_FK = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    position_FK = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        update_last_activity = kwargs.pop("update_last_activity", False)

        if update_last_activity:
            self.update_last_activity()
            return

        previous = type(self).objects.filter(pk=self.pk).values_list("image", flat=True).first() if self.pk else None
        changed = self.image and self.image.name != "profile.webp" and (not self.image._committed or previous != self.image.name)

        super(Profile, self).save(*args, **kwargs)

        if changed and self.image.storage.exists(self.image.name):
            resize_image(self.image.path, 300)
            crop_image(self.image.path, 300)
        if previous and previous != "profile.webp" and previous != self.image.name:
            storage = self.image.storage
            transaction.on_commit(lambda: storage.delete(previous))

    def update_last_activity(self):
        self.last_activity = timezone.now()
        type(self).objects.filter(pk=self.pk).update(last_activity=self.last_activity)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["-id"]

    def __str__(self):
        return self.user_FK.username
