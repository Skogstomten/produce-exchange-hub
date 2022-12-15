from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("company/<int:company_id>", views.company, name="company"),
    path("company/<int:company_id>/edit", views.EditCompanyView.as_view(), name="edit_company"),
    path(
        "company/<int:company_id>/profile-picture",
        views.CompanyProfilePictureView.as_view(),
        name="company_profile_picture",
    ),
]
