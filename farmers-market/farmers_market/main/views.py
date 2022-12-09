"""Views for main module"""
from os import path
from pathlib import Path

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company
from .forms import UpdateCompanyForm, UploadFileForm
from .decorators import company_admin_required
from .utils import get_language
from .mixins import CompanyAdminRequiredMixin


@login_required()
@company_admin_required()
def upload_company_profile_picture(request: HttpRequest, company_id: int):
    """
    Uploads a profile picture for company.
    """
    if request.method == "POST":
        company = Company.get(company_id, get_language(request))
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            file_name = path.join(settings.COMPANY_PROFILE_PICTURE_DIR, company.id, Path(file.name).suffix)
            with open(file_name, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            company.profile_picture_url = file_name
            company.save()
    return redirect(reverse("main:edit_company", args=(company_id,)))


def index(request: HttpRequest):
    companies = Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
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
            {"company": company, "update_company_form": form, "upload_profile_picture_form": UploadFileForm()},
            status=status,
        )
