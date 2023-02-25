from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("companies/new", views.NewCompanyView.as_view(), name="new_company"),
    path("companies/<int:company_id>", views.company_view, name="company"),
    path("companies/<int:company_id>/edit", views.EditCompanyView.as_view(), name="edit_company"),
    path("companies/<int:company_id>/users", views.CompanyUsersView.as_view(), name="company_users"),
    path(
        "companies/<int:company_id>/users/<int:user_id>/delete", views.delete_company_user, name="delete_company_user"
    ),
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
    path("companies/<int:company_id>/deactivate", views.deactivate_company, name="deactivate_company"),
    path("companies/<int:company_id>/orders/add-sell-order", views.add_order, name="add_sell_order"),
    path("companies/<int:company_id>/orders/add_buy_order", views.add_order, name="add_buy_order"),
    path("companies/<int:company_id>/orders/update", views.update_orders, name="update_orders"),
    path("companies/<int:company_id>/orders/<int:order_id>/delete", views.delete_order, name="delete_order"),
]
