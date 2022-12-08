from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple

from .models import Company, CompanyType, Language


class UpdateCompanyForm(ModelForm):
    company_types = ModelMultipleChoiceField(
        queryset=CompanyType.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True
    )
    content_languages = ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Company
        fields = ["name", "company_types", "content_languages", "external_website_url"]
