from typing import Iterable

from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from .models import Company
from .utils import get_language


class CompanyRoleRequiredDecorator:
    def __init__(self, pk_name: str, company_roles: list[str]):
        self.pk_name = pk_name
        self.company_roles = company_roles

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            request = next(arg for arg in args if isinstance(arg, HttpRequest))
            pk = kwargs.get(self.pk_name)
            company = Company.get(pk, get_language(request))
            if request.user.is_staff or (
                request.user.is_authenticated and company.has_company_role(request.user, self.company_roles)
            ):
                return function(*args, **kwargs)
            if not request.user.is_authenticated:
                return redirect(reverse("authentication:login"))
            return HttpResponseForbidden()

        return wrapper


def company_role_required(pk_name: str = "company_id", company_roles: Iterable[str] = ("company_admin",)):
    """Checks if user has one of specified roles. Company admin is always included."""
    company_roles = list(company_roles)
    if "company_admin" not in company_roles:
        company_roles.append("company_admin")
    if callable(pk_name):
        return CompanyRoleRequiredDecorator("company_id", company_roles)(pk_name)
    return CompanyRoleRequiredDecorator(pk_name, company_roles)
