from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import DetailView

from .models import Company


def index(request: HttpRequest):
    companies = Company.objects.filter(status__status_name="active").order_by("-activation_date")[:10]
    return render(request, "main/index.html", {"companies": companies})


class CompanyView(DetailView):
    model = Company
    template_name = "main/company.html"