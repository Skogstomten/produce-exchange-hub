"""Views for main module"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
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
        
        return self._render(request, UpdateCompanyForm(instance=company), company)

    def post(self, request: HttpRequest, pk: int):
        company = get_object_or_404(Company, pk=pk)
        update_company_form = UpdateCompanyForm(data=request.POST, instance=company)
        if not update_company_form.is_valid():
            error_str = ", ".join([f"{key}: {value}" for key, value in update_company_form.errors.items()])
            raise Exception(error_str)
        update_company_form.save()

        if not company.is_company_admin(request.user):
            return HttpResponseForbidden()  # TODO: Make better

        return self._render(request, update_company_form, company, 202)
    
    def _render(self, request: HttpRequest, form: UpdateCompanyForm, company: Company, status: int = 200) -> HttpResponse:
        return render(request, self.template_name, {"company": company, "update_company_form": form}, status=status)


def _get_language(request: HttpRequest) -> str:
    return request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
