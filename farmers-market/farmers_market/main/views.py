from django.shortcuts import render
from django.http import HttpRequest


def index(request: HttpRequest):
    return render(request, "main/index.html", {})


def register(request: HttpRequest):
    return render(request, "main/register.html", {})


def login(request: HttpRequest):
    return render(request, "main/login.html", {})
