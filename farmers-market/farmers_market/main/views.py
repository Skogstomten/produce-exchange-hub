"""Views for main module."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from shared.decorators import post_only
from .decorators import company_role_required
from .forms import (
    UpdateCompanyForm,
    UploadCompanyProfilePictureForm,
    NewCompanyForm,
    ContactForm,
    AddressForm,
    AddCompanyUserForm,
    SellOrderForm,
    BuyOrderForm,
    OrderForm,
    OrderFormSet,
)
from .mixins import CompanyRoleRequiredMixin
from .models import Company, CompanyStatus, Contact, Address, CompanyUser, OrderType, Order
from .utils import get_language


@company_role_required()
def upload_company_profile_picture(request: HttpRequest, company_id: int):
    """Upload a profile picture for company."""
    company = Company.get(company_id, get_language(request))
    form = UploadCompanyProfilePictureForm(company, request.POST, request.FILES)
    if form.is_valid():
        form.save()
    else:
        return HttpResponseBadRequest()
    return redirect(reverse("main:edit_company", args=(company_id,)))


def index(request: HttpRequest):
    return render(request, "main/index.html", {"companies": Company.get_newest(get_language(request))})


def company_view(request: HttpRequest, company_id: int):
    company = Company.get(company_id, get_language(request))
    return render(
        request,
        "main/company.html",
        {
            "company": company,
            "user_is_company_admin": company.is_company_admin(request.user) if request.user.is_authenticated else False,
        },
    )


@post_only
@company_role_required
def add_contact(request: HttpRequest, company_id: int):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    form.save()
    return redirect(reverse("main:edit_company", args=(company_id,)))


@post_only
@company_role_required
def delete_contact(request: HttpRequest, company_id: int, contact_id: int):
    try:
        contact = Contact.objects.get(pk=contact_id, company__id=company_id)
        contact.delete()
    except Contact.DoesNotExist:
        return HttpResponseNotFound()
    return redirect(reverse("main:edit_company", args=(company_id,)))


@post_only
@company_role_required
def add_address(request: HttpRequest, company_id: int):
    form = AddressForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()
    form.save()
    return redirect(reverse("main:edit_company", args=(company_id,)))


@post_only
@company_role_required()
def delete_address(request: HttpRequest, company_id: int, address_id: int):
    try:
        address = Address.objects.get(pk=address_id, company__id=company_id)
        address.delete()
    except Address.DoesNotExist:
        return HttpResponseNotFound()
    return redirect(reverse("main:edit_company", args=(company_id,)))


class EditCompanyView(CompanyRoleRequiredMixin, View):
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
        context = {
            "company": company,
            "update_company_form": UpdateCompanyForm(instance=company),
            "upload_profile_picture_form": UploadCompanyProfilePictureForm(instance=company),
            "add_contact_form": ContactForm(instance=Contact(company=company)),
            "add_address_form": AddressForm(instance=Address(company=company)),
            "edit_sell_orders_formset": OrderFormSet(
                queryset=company.orders.filter(order_type=OrderType.SELL), initial=[{"company": company.id}]
            ),
            "is_company_admin": company.is_company_admin(request.user),
        }

        if company.is_producer():
            context.update(
                {
                    "is_producer": True,
                    "add_sell_order_form": SellOrderForm(company),
                    "sell_order_post_url": reverse("main:add_sell_order", args=(company.id,)),
                    "add_sell_order_title": _("Add sell order"),
                }
            )

        if company.is_buyer():
            context.update(
                {
                    "is_buyer": True,
                    "add_buy_order_form": BuyOrderForm(company),
                    "buy_order_post_url": reverse("main:add_buy_order", args=(company.id,)),
                    "add_buy_order_title": _("Add buy order"),
                }
            )

        return render(
            request,
            self.template_name,
            context,
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


@post_only
@company_role_required
def activate_company(request: HttpRequest, company_id: int):
    company = Company.get(company_id, get_language(request))
    company.status = CompanyStatus.get(CompanyStatus.StatusName.active)
    company.save()
    return redirect(reverse("main:edit_company", args=(company.id,)))


class CompanyUsersView(CompanyRoleRequiredMixin, View):
    template_name = "main/company_users.html"

    def get(self, request: HttpRequest, company_id: int):
        company = Company.get(company_id)
        return self._render(request, company, AddCompanyUserForm(company))

    def post(self, request: HttpRequest, company_id: int):
        company = Company.get(company_id)
        form = AddCompanyUserForm(company, request.POST)
        errors = None
        if form.is_valid():
            form.save()
            form = AddCompanyUserForm(company)
        else:
            errors = form.errors
        return self._render(request, company, form, errors)

    def _render(self, request: HttpRequest, company: Company, form: AddCompanyUserForm, errors=None):
        return render(request, self.template_name, {"company": company, "add_user_form": form, "errors": errors})


@post_only
@company_role_required
def delete_company_user(request: HttpRequest, company_id: int, user_id: int):
    company_user = get_object_or_404(CompanyUser, company__id=company_id, user__id=user_id)
    company_user.delete()
    return redirect(reverse("main:company_users", args=(company_id,)))


@post_only
@company_role_required(company_roles=["order_admin"])
def add_order(request: HttpRequest, company_id: int):
    company = get_object_or_404(Company, pk=company_id)
    form = OrderForm(company, data=request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse("main:edit_company", args=(company.id,)))


@post_only
@company_role_required(company_roles=["order_admin"])
def update_orders(request: HttpRequest, company_id: int):
    company = get_object_or_404(Company, pk=company_id)
    formset = OrderFormSet(request.POST)
    if formset.is_valid():
        formset.save()
    return redirect(reverse("main:edit_company", args=(company.id,)))


@post_only
@company_role_required
def deactivate_company(request: HttpRequest, company_id: int):
    company = get_object_or_404(Company, pk=company_id)
    company.status = CompanyStatus.get(CompanyStatus.StatusName.deactivated)
    company.save()
    return redirect(reverse("main:edit_company", args=(company.id,)))


@post_only
@company_role_required(company_roles=("order_admin",))
def delete_order(request: HttpRequest, company_id: int, order_id: int):
    company = get_object_or_404(Company, id=company_id)
    order = get_object_or_404(Order, id=order_id, company=company)
    order.delete()
    return redirect(reverse("main:edit_company", args=(company_id,)))
