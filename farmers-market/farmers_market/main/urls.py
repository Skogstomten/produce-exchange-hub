from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/register/", views.register, name="register"),
    path("auth/login/", views.login, name="login"),
]
