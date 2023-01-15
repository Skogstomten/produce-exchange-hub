from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("companies/new", views.NewCompanyView.as_view(), name="new_company"),
    path("companies/<int:company_id>", views.company, name="company"),
    path("companies/<int:company_id>/edit", views.EditCompanyView.as_view(), name="edit_company"),
    path("companies/<int:company_id>/users", views.company_users, name="company_users"),
    path("companies/<int:company_id>/contact", views.add_contact, name="add_contact"),
    path("companies/<int:company_id>/contact/<int:contact_id>", views.delete_contact, name="delete_contact"),
    path("companies/<int:company_id>/addresses", views.add_address, name="add_address"),
    path("companies/<int:company_id>/addresses/<int:address_id>", views.delete_address, name="delete_address"),
    path(
        "companies/<int:company_id>/profile-picture",
        views.upload_company_profile_picture,
        name="company_profile_picture",
    ),
    path("companies/<int:company_id>/activate", views.activate_company, name="activate_company"),
]
