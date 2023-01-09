from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseNotFound
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import login, logout as logout_user

from django.utils.translation import gettext_lazy as _

from .decorators import self
from .forms import RegisterForm, LoginForm, UploadProfilePictureForm, UserForm, ExtendedUserForm
from .models import ExtendedUser


class UserProfileView(View):
    @self
    def get(self, request: HttpRequest, user_id: int):
        try:
            ext_user = ExtendedUser.objects.get(user__id=user_id)
        except ExtendedUser.DoesNotExist:
            ext_user = ExtendedUser(user=request.user)
        return render(
            request,
            "authentication/user_profile.html",
            {
                "profile_picture_form": UploadProfilePictureForm(instance=ext_user),
                "user_form": UserForm(request.user),
                "extended_user_form": ExtendedUserForm(instance=ext_user),
            },
        )


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
        return render(request, self.template_name, {"login_form": LoginForm(request.GET.get("return_url", None))})

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid(request):
            login(request, form.user)
            return_url = form.get_return_url()
            if return_url:
                return redirect(return_url)
            return redirect(reverse("main:index"))
        return render(request, self.template_name, {"login_form": form, "errors": form.errors}, status=400)


@self
def upload_profile_picture(request: HttpRequest, user_id: int):
    if request.method != "POST":
        return HttpResponseNotFound()
    try:
        ext_user = ExtendedUser.objects.get(user__id=user_id)
    except ExtendedUser.DoesNotExist:
        ext_user = ExtendedUser(user=request.user)
    form = UploadProfilePictureForm(request.POST, request.FILES, instance=ext_user)
    if form.is_valid():
        form.save()
    return redirect(reverse("authentication:user_profile", args=(user_id,)))


def logout(request: HttpRequest):
    logout_user(request)
    return redirect(reverse("main:index"))
