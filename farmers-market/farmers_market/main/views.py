"""Views for main module"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


def index(request: HttpRequest):
    companies = models.Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
    return render(request, "main/index.html", {"companies": companies})


class CompanyView(View):
    def get(self, request: HttpRequest, pk: int):
        company = get_object_or_404(models.Company, pk=pk)
        company.description = company.get_description(
            request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
        )
        return render(
            request,
            "main/company.html",
            {
                "company": company,
                "user_is_company_admin": company.is_company_admin(request.user),
            },
        )


class EditCompanyView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int):
        company = get_object_or_404(models.Company, pk=pk)
        content_languages = [language.iso_639_1 for language in company.content_languages.all()]
        if company.is_company_admin(request.user):
            return render(
                request,
                "main/edit_company.html",
                {
                    "company": company,
                    "company_types": models.CompanyType.objects.all(),
                    "languages": [
                        {"id": language.id, "name": language.name, "checked": language.iso_639_1 in content_languages}
                        for language in models.Language.objects.all()
                    ],
                },
            )

        # TODO: Make a better forbidden page
        return HttpResponseForbidden()
