from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Position, AreaDocente
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from core.permissions import es_administrador
from CliniTensDocenteApp.upload_validation import validar_archivo


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class UserCreateForm(UserCreationForm, UserUpdateForm):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = UserUpdateForm.Meta.fields + ["password1", "password2"]

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        label="Imagen",
        widget=forms.FileInput(attrs={"class": "hidden", "id": "id_image"}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ["image"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and not getattr(image, "_committed", False) and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "El tamaño del archivo de imagen no debe exceder los 5 MB."
            )
        if image and not getattr(image, "_committed", False):
            validar_archivo(image)
        return image


class CargoSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        instance = getattr(value, "instance", None)
        option["attrs"]["data-docente"] = "true" if instance and instance.permission_code == "MANAGER" else "false"
        return option


class ProfileCreateForm(ProfileUpdateForm):
    position_FK = forms.ModelChoiceField(
        label="Cargo",
        queryset=Position.objects.none(),
        widget=CargoSelect(
            attrs={
                "class": "bg-white focus:outline-hidden border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700 mb-3"
            }
        ),
    )

    class Meta(ProfileUpdateForm.Meta):
        fields = ProfileUpdateForm.Meta.fields + ["position_FK", "area_docente"]
        widgets = {"area_docente": forms.Select(attrs={"class": "input"})}
        help_texts = {"area_docente": "Obligatoria para las cuentas docentes. Ambos habilita las dos áreas."}

    def __init__(self, *args, actor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if actor is not None and es_administrador(actor):
            cargos = ["RESTRICTED", "MANAGER"]
            if actor.is_superuser:
                cargos.append("ADMIN")
            self.fields["position_FK"].queryset = Position.objects.filter(permission_code__in=cargos)

    def clean(self):
        cleaned = super().clean()
        posicion = cleaned.get("position_FK")
        if posicion and posicion.permission_code == "MANAGER" and not cleaned.get("area_docente"):
            self.add_error("area_docente", "Selecciona el área del docente.")
        elif posicion and posicion.permission_code != "MANAGER":
            cleaned["area_docente"] = ""
        return cleaned


class AreaDocenteForm(forms.ModelForm):
    area_docente = forms.ChoiceField(
        label="Área docente", choices=AreaDocente.choices,
        widget=forms.Select(attrs={"class": "input"}),
        help_text="Farmacia habilita FarmaTEF. Enfermería habilita CliniTENS. Ambos habilita las dos áreas.",
    )

    class Meta:
        model = Profile
        fields = ["area_docente"]
