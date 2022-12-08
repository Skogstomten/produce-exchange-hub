from django.forms import ModelForm

from .models import Company


class UpdateCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_types", "content_languages", "external_website_url"]
