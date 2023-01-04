"""Views for main module"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Contact
from .forms import UpdateCompanyForm, UploadCompanyProfilePictureForm, NewCompanyForm, AddContactForm
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


@company_admin_required()
def add_contact(request: HttpRequest, company_id: int):
    if request.method != "POST":
        return HttpResponseNotFound()
    form = AddContactForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    form.save()
    return redirect(reverse("main:edit_company", args=(company_id,)))


@company_admin_required()
def delete_contact(request: HttpRequest, company_id: int, contact_id: int):
    if request.method != "POST":
        return HttpResponseNotFound()
    try:
        contact = Contact.objects.get(pk=contact_id, company__id=company_id)
        contact.delete()
    except Contact.DoesNotExist:
        return HttpResponseNotFound()
    return redirect(reverse("main:edit_company", args=(company_id,)))


class EditCompanyView(CompanyAdminRequiredMixin, View):
    template_name = "main/edit_company.html"

    def get(self, request: HttpRequest, company_id: int):
        company = get_object_or_404(Company, pk=company_id)
        return self._render(request, company)

    def post(self, request: HttpRequest, company_id: int):
        company = get_object_or_404(Company, pk=company_id)
        update_company_form = UpdateCompanyForm(data=request.POST, instance=company)
        if not update_company_form.is_valid():
            error_str = ", ".join([f"{key}: {value}" for key, value in update_company_form.errors.items()])
            raise Exception(error_str)
        update_company_form.save()
        return self._render(request, company, 202)

    def _render(self, request: HttpRequest, company: Company, status: int = 200) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "company": company,
                "contacts": Contact.all_for(company),
                "update_company_form": UpdateCompanyForm(instance=company),
                "upload_profile_picture_form": UploadCompanyProfilePictureForm(instance=company),
                "add_contact_form": AddContactForm(instance=Contact(company=company)),
            },
            status=status,
        )


class NewCompanyView(LoginRequiredMixin, View):
    template_name = "main/new_company.html"

    def get(self, request: HttpRequest):
        return self._render_get(request)

    def post(self, request: HttpRequest):
        form = NewCompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
        else:
            return self._render_get(request)
        return redirect(reverse("main:edit_company", args=(company.id,)))

    def _render_get(self, request: HttpRequest):
        form = NewCompanyForm()
        form.fields.get("user_id").initial = request.user.id
        return render(request, self.template_name, {"new_company_form": form})
