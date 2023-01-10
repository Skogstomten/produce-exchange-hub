from django.urls import path

from . import views

app_name = "authentication"
urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout, name="logout"),
    path("user/<int:user_id>", views.user_profile_view, name="user_profile"),
    path("user/<int:user_id>/profile_picture", views.upload_profile_picture, name="upload_profile_picture"),
]
