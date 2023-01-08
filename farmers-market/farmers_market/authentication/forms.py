from typing import Tuple

from django.forms import (
    Form,
    ModelForm,
    FileField,
    FloatField,
    CharField,
    EmailField,
    FileInput,
    PasswordInput,
    HiddenInput,
    ValidationError,
)
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import ExtendedUser


class RegisterForm(Form):
    email = EmailField(required=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    password = CharField(required=True, widget=PasswordInput)
    confirm_password = CharField(required=True, widget=PasswordInput)
    county = CharField(required=False)

    def is_valid(self) -> bool:
        if self.cleaned_data["password"] == self.cleaned_data["confirm_password"]:
            return super().is_valid()
        return False

    def save(self) -> Tuple[User, ExtendedUser]:
        user = User.objects.create(**self.cleaned_data)
        ext_user = ExtendedUser.objects.create(user=user, **self.cleaned_data)
        return user, ext_user

    def get_email(self) -> str:
        return self.cleaned_data["email"]

    def get_password(self) -> str:
        return self.cleaned_data["password"]


class LoginForm(Form):
    email = EmailField(required=True)
    password = CharField(required=True, widget=PasswordInput)
    return_url = CharField(required=False, widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return_url = kwargs.pop("return_url", None)
        if return_url:
            self.fields["return_url"].initial = return_url
        self.fields["email"].widget.attrs.update({"autofocus": "autofocus"})

    def is_valid(self, request: HttpRequest) -> bool:
        if not super().is_valid():
            return False
        self.user = authenticate(request, **self.get_credentials())
        if not self.user:
            self.add_error("password", ValidationError(_("Invalid username or password"), code="invalid_login"))
            return False
        return True

    def get_credentials(self) -> dict[str, str]:
        return {"username": self.cleaned_data.get("email"), "password": self.cleaned_data.get("password")}

    def get_return_url(self) -> str | None:
        return self.cleaned_data.get("return_url", None)


class UploadProfilePictureForm(ModelForm):
    x = FloatField(widget=HiddenInput)
    y = FloatField(widget=HiddenInput)
    width = FloatField(widget=HiddenInput)
    height = FloatField(widget=HiddenInput)
    profile_picture = FileField(required=True, label=_("Upload profile picture"), widget=FileInput)

    class Meta:
        model = ExtendedUser
        fields = ["profile_picture", "x", "y", "width", "height"]

    def save(self):
        user: ExtendedUser = super().save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        Image.open(user.profile_picture).crop((x, y, x + width, y + height)).resize((300, 300), Image.ANTIALIAS).save(
            user.profile_picture.path
        )

        return user
