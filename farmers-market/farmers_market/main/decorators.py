from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from .models import Company
from .utils import get_language


class CompanyAdminRequiredDecorator:
    def __init__(self, pk_name: str):
        self.pk_name = pk_name

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            request = next(arg for arg in args if isinstance(arg, HttpRequest))
            pk = kwargs.get(self.pk_name)
            company = Company.get(pk, get_language(request))
            if request.user.is_staff or (request.user.is_authenticated and company.is_company_admin(request.user)):
                return function(*args, **kwargs)
            if not request.user.is_authenticated:
                return redirect(reverse("authentication:login"))
            return HttpResponseForbidden()

        return wrapper


def company_admin_required(pk_name: str = "company_id"):
    if callable(pk_name):
        return CompanyAdminRequiredDecorator("company_id")(pk_name)
    return CompanyAdminRequiredDecorator(pk_name)
