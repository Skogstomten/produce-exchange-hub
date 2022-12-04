from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("company/<int:pk>", views.CompanyView.as_view(), name="company")
]
