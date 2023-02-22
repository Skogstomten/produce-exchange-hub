from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import (
    Form,
    ModelForm,
    CharField,
    EmailField,
    ModelChoiceField,
    PasswordInput,
    HiddenInput,
    RadioSelect,
    ValidationError,
)
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shared.forms import UploadCroppedPictureModelForm
from shared.models import Country
from .models import ExtendedUser


class RegisterForm(Form):
    email = EmailField(required=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    password = CharField(required=True, widget=PasswordInput)
    confirm_password = CharField(required=True, widget=PasswordInput)
    county = CharField(required=False)

    def is_valid(self) -> bool:
        if super().is_valid():
            if self.cleaned_data["password"] == self.cleaned_data["confirm_password"]:
                return True
            else:
                self.add_error(
                    "confirm_password",
                    ValidationError(_("Confirm password does not match password."), "password_no_match"),
                )
        return False

    def save(self) -> User:
        user = User.objects.create_user(
            self.cleaned_data.get("email"),
            self.cleaned_data.get("email"),
            self.cleaned_data.get("password"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
        )
        ExtendedUser.create_ext_user(user, self.cleaned_data.get("county", None))
        return user

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
        self.user = None

    def is_valid(self, request: HttpRequest = None) -> bool:
        if not super().is_valid():
            return False
        if not request:
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


class UploadProfilePictureForm(UploadCroppedPictureModelForm):
    def __init__(self, instance: ExtendedUser, data=None, files=None, *args, **kwargs):
        super().__init__(
            reverse("authentication:upload_profile_picture", args=(instance.user.id,)),
            instance,
            data,
            files,
            *args,
            **kwargs
        )

    class Meta(UploadCroppedPictureModelForm.Meta):
        model = ExtendedUser


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def save(self, commit: bool = ...) -> Any:
        user = super().save(False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ExtendedUserForm(ModelForm):
    country = ModelChoiceField(Country.objects.all(), widget=RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].initial = Country.objects.first()

    class Meta:
        model = ExtendedUser
        fields = ["county", "country"]
