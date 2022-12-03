from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class RegisterView(TemplateView):
    template_name = "authentication/register.html"

    def post(self, request):
        User.objects.create(**request.POST)
        return_url = request.POST["return_url"]
        if return_url:
            return redirect(return_url)
        else:
            return redirect(reverse("main:index"))


class LoginView(TemplateView):
    template_name = "authentication/login.html"

    def post(self, request: HttpRequest):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(user)
            return_url = request.POST.get("return_url", None)
            if return_url:
                return redirect(return_url)
        else:
            return render(request, self.template_name, {"message": "Unable to authenticate user. Please check your information."})


def logout(request: HttpRequest):
    logout(request)
    return redirect(reverse("main:index"))
