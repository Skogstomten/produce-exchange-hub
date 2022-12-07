"""Views for main module"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


def _get_edit_company_template_context(company: models.Company) -> dict:
    content_languages = [language.iso_639_1 for language in company.content_languages.all()]
    company_types = [company_type.type_name for company_type in company.company_types.all()]
    return {
                "company": company,
                "company_types": [
                    {
                        "id": company_type.id,
                        "type_name": company_type.type_name,
                        "checked": "checked" if company_type.type_name in company_types else "",
                    }
                    for company_type in models.CompanyType.objects.all()
                ],
                "languages": [
                    {
                        "id": language.id,
                        "name": language.name,
                        "checked": "checked" if language.iso_639_1 in content_languages else "",
                    }
                    for language in models.Language.objects.all()
                ],
            }


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
    template_name = "main/edit_company.html"

    def get(self, request: HttpRequest, pk: int):
        company = get_object_or_404(models.Company, pk=pk)
        
        if not company.is_company_admin(request.user):
            return HttpResponseForbidden()  # TODO: Make better

        return render(
            request,
            self.template_name,
            _get_edit_company_template_context(company),
        )

    def post(self, request: HttpRequest, pk: int):
        company = get_object_or_404(models.Company, pk=pk)
        company.name = request.POST.get("company_name").strip()
        company.external_website_url = request.POST.get("external_website_url").strip()

        current_company_type_ids = set(company_type.id for company_type in company.company_types.all())
        selected_company_type_ids = set(
            int(company_type_id) for company_type_id in request.POST.getlist("company_types")
        )

        for current_company_type_id in current_company_type_ids:
            if not current_company_type_id in selected_company_type_ids:
                company.company_types.remove(models.CompanyType.objects.get(pk=current_company_type_id))

        for selected_company_type_id in selected_company_type_ids:
            if not selected_company_type_id in current_company_type_ids:
                company.company_types.add(models.CompanyType.objects.get(pk=selected_company_type_id))

        current_language_ids = set(language.id for language in company.content_languages.all())
        selected_language_ids = set(int(language_id) for language_id in request.POST.getlist("content_languages"))

        for current_language_id in current_language_ids:
            if not current_language_id in selected_language_ids:
                company.content_languages.remove(models.Language.objects.get(current_language_id))

        for selected_language_id in selected_language_ids:
            if not selected_language_id in current_language_ids:
                company.content_languages.add(models.Language.objects.get(pk=selected_company_type_id))

        company.save()

        return render(request, self.template_name, _get_edit_company_template_context(company), status=202)
