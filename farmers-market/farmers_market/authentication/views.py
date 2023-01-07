from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout as logout_user

from django.utils.translation import gettext_lazy as _

from .decorators import self
from .forms import RegisterForm, LoginForm


class UserProfileView(View):
    @self()
    def get(self, request: HttpRequest, user_id: int):
        return render(request, "authentication/user_profile.html")


class RegisterView(View):
    template_name = "authentication/register.html"

    def get(self, request: HttpRequest):
        form = RegisterForm()
        return render(request, self.template_name, {"register_form": form})

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user, _ = form.save()
            login(request, user)
            return redirect(reverse("authentication:user_profile", args=(user.id,)))
        return render(request, self.template_name, {"register_form": form})


class LoginView(View):
    template_name = "authentication/login.html"

    def get(self, request: HttpRequest):
        return render(
            request, self.template_name, {"login_form": LoginForm({"return_url": request.GET.get("return_url", None)})}
        )

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.get_credentials())
            if user:
                login(request, user)
                return_url = form.get_return_url()
                if return_url:
                    return redirect(return_url)
                return redirect(reverse("main:index"))
            else:
                form.add_error(error=_("Invalid username or password"))
                return render(
                    request,
                    self.template_name,
                    {"login_form": form},
                )
        return render(request, self.template_name, {"login_form": form})


def logout(request: HttpRequest):
    logout_user(request)
    return redirect(reverse("main:index"))
