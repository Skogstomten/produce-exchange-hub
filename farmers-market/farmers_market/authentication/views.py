from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout as logout_user

from .decorators import self
from .forms import RegisterForm


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
            user = authenticate(username=form.get_email(), password=form.get_password())
            return redirect(reverse("authentication:user_profile", args=(user.id,)))
        return render(request, self.template_name, {"register_form": form})


class LoginView(TemplateView):
    template_name = "authentication/login.html"

    def post(self, request: HttpRequest):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return_url = request.POST.get("return_url", None)
            if return_url:
                return redirect(return_url)
            return redirect(reverse("main:index"))
        else:
            return render(
                request, self.template_name, {"message": "Unable to authenticate user. Please check your information."}
            )


def logout(request: HttpRequest):
    logout_user(request)
    return redirect(reverse("main:index"))
