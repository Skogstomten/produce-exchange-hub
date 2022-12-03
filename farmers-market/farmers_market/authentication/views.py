from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import TemplateView


class RegisterView(TemplateView):
    template_name = "authentication/register.html"


class LoginView(TemplateView):
    template_name = "authentication/login.html"


def logout(request: HttpRequest):
    pass
