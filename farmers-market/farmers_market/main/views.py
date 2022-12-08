"""Views for main module"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, CompanyType, Language
from .forms import UpdateCompanyForm


@login_required()
def upload_company_profile_picture(request: HttpRequest, company_id: int):
    pass


def index(request: HttpRequest):
    companies = Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
    return render(request, "main/index.html", {"companies": companies})


class CompanyView(View):
    def get(self, request: HttpRequest, pk: int):
        company = Company.get(pk, _get_language(request))
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
        company = get_object_or_404(Company, pk=pk)

        if not company.is_company_admin(request.user):
            return HttpResponseForbidden()  # TODO: Make better
        
        update_company_form = UpdateCompanyForm(instance=company)

        return render(
            request,
            self.template_name,
            {"update_company_form": update_company_form, **_get_edit_company_template_context(company)},
        )

    def post(self, request: HttpRequest, pk: int):
        company = get_object_or_404(Company, pk=pk)
        company.name = request.POST.get("company_name").strip()
        company.external_website_url = request.POST.get("external_website_url").strip()

        _sync_checked_with_related_table(company.company_types, request, "company_types", CompanyType.objects)
        _sync_checked_with_related_table(company.content_languages, request, "content_languages", Language.objects)

        company.save()

        return render(request, self.template_name, _get_edit_company_template_context(company), status=202)


def _sync_checked_with_related_table(related_table, request, element_name, objects):
    current_ids = set(item.id for item in related_table.all())
    selected_ids = set(int(value) for value in request.POST.getlist(element_name))
    _compare_and_update(current_ids, selected_ids, related_table.remove, objects)
    _compare_and_update(selected_ids, current_ids, related_table.add, objects)


def _compare_and_update(first, second, operation, objects):
    for val in first:
        if not val in second:
            operation(objects.get(pk=val))


def _get_language(request: HttpRequest) -> str:
    return request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)


def _get_edit_company_template_context(company: Company) -> dict:
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
            for company_type in CompanyType.objects.all()
        ],
        "languages": [
            {
                "id": language.id,
                "name": language.name,
                "checked": "checked" if language.iso_639_1 in content_languages else "",
            }
            for language in Language.objects.all()
        ],
    }
