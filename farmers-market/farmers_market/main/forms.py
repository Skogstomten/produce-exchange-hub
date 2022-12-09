from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, FileField, Form
from django.utils.translation import gettext_lazy as _

from .models import Company, CompanyType, Language


class UpdateCompanyForm(ModelForm):
    company_types = ModelMultipleChoiceField(
        queryset=CompanyType.objects.all(), widget=CheckboxSelectMultiple, required=True
    )
    content_languages = ModelMultipleChoiceField(
        queryset=Language.objects.all(), widget=CheckboxSelectMultiple, required=True
    )

    class Meta:
        model = Company
        fields = ["name", "company_types", "content_languages", "external_website_url"]


class UploadFileForm(Form):
    file = FileField(required=True, label=_("upload_profile_picture_label"))
