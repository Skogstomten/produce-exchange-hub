from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from .models import Company
from .utils import get_language


def company_admin_required(pk_name: str = "company_id"):
    def decorator(function):
        def wrapper(*args, **kwargs):
            # print(f"*args={', '.join(str(arg) for arg in args)}, **kwargs={', '.join(f'{str(k)}: {str(v)}' for k, v in kwargs.items())}")

            request: HttpRequest = args[0]
            pk = kwargs.get(pk_name)
            if not request.user.is_authenticated:
                return redirect(reverse("authentication:login"))

            company = Company.get(pk, get_language(request))
            if not company.is_company_admin(request.user):
                return HttpResponseForbidden()

            return function(*args, **kwargs)

        return wrapper

    return decorator
