from django.shortcuts import render
from django.http import HttpRequest


def register(request: HttpRequest):
    return render(request, "authentication/register")


def login(request: HttpRequest):
    return render(request, "athentication/login")


def logout(request: HttpRequest):
    return render(request, "authentication/logout")
