from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.views.generic import View
from django.conf import settings

from .models import Company


def index(request: HttpRequest):
    companies = Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
    return render(request, "main/index.html", {"companies": companies})


class CompanyView(View):
    model = Company
    template_name = "main/company.html"

    def get(self, request: HttpRequest, pk: int):
        company = get_object_or_404(Company, pk=pk)
        company.description = company.get_description(request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE))
        return render(
            request,
            self.template_name,
            {
                "company": company,
                "user_is_company_admin": company.is_company_admin(request.user),
            }
        )
