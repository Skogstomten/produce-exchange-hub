"""Views for main module"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company
from .forms import UpdateCompanyForm, UploadCompanyProfilePictureForm
from .decorators import company_admin_required
from .utils import get_language
from .mixins import CompanyAdminRequiredMixin


class CompanyProfilePictureView(View):
    @company_admin_required()
    def post(self, request: HttpRequest, company_id: int):
        """Upload a profile picture for company."""
        company = Company.get(company_id, get_language(request))
        form = UploadCompanyProfilePictureForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
        else:
            return form.errors
        return redirect(reverse("main:edit_company", args=(company_id,)))


def index(request: HttpRequest):
    companies = Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
    for company in companies:
        company.description = company.get_description(get_language(request))
    return render(request, "main/index.html", {"companies": companies})


def company(request: HttpRequest, company_id: int):
    company = Company.get(company_id, get_language(request))
    return render(
        request,
        "main/company.html",
        {"company": company, "user_is_company_admin": company.is_company_admin(request.user)},
    )


class EditCompanyView(LoginRequiredMixin, CompanyAdminRequiredMixin, View):
    template_name = "main/edit_company.html"

    def get(self, request: HttpRequest, company_id: int):
        company = get_object_or_404(Company, pk=company_id)
        return self._render(request, UpdateCompanyForm(instance=company), company)

    def post(self, request: HttpRequest, company_id: int):
        company = get_object_or_404(Company, pk=company_id)
        update_company_form = UpdateCompanyForm(data=request.POST, instance=company)
        if not update_company_form.is_valid():
            error_str = ", ".join([f"{key}: {value}" for key, value in update_company_form.errors.items()])
            raise Exception(error_str)
        update_company_form.save()
        return self._render(request, update_company_form, company, 202)

    def _render(
        self, request: HttpRequest, form: UpdateCompanyForm, company: Company, status: int = 200
    ) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "company": company,
                "update_company_form": form,
                "upload_profile_picture_form": UploadCompanyProfilePictureForm(instance=company),
            },
            status=status,
        )
