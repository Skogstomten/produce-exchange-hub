from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout as logout_user
from django.contrib.auth.models import User


class RegisterView(TemplateView):
    template_name = "authentication/register.html"

    def post(self, request):
        User.objects.create_user(request.POST.get("email"), request.POST.get("email"), request.POST.get("password"), first_name=request.POST.get("first_name"), last_name=request.POST.get("last_name"))
        return redirect(reverse("authentication:login"))


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
            return render(request, self.template_name, {"message": "Unable to authenticate user. Please check your information."})


def logout(request: HttpRequest):
    logout_user(request)
    return redirect(reverse("main:index"))
