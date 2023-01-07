from typing import Tuple

from django.forms import Form, CharField, EmailField, PasswordInput
from django.contrib.auth.models import User

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

    def get_credentials(self) -> dict[str, str]:
        return {"username": self.cleaned_data["email"], "password": self.cleaned_data["password"]}
