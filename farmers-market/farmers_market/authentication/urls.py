from django.urls import path

from .views import RegisterView, LoginView, logout

app_name = "authentication"
urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout, name="logout"),
]
