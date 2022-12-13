from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, FileField, FloatField, HiddenInput
from django.utils.translation import gettext_lazy as _

from PIL import Image

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


class UploadCompanyProfilePictureForm(ModelForm):
    x = FloatField(widget=HiddenInput)
    y = FloatField(widget=HiddenInput)
    width = FloatField(widget=HiddenInput)
    height = FloatField(widget=HiddenInput)
    profile_picture = FileField(required=True, label=_("upload_profile_picture_label"))

    class Meta:
        model = Company
        fields = ["profile_picture", "x", "y", "width", "height"]

    def save(self):
        company: Company = super().save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        Image.open(company.profile_picture).crop((x, y, x+width, y+height)).resize((200, 200), Image.ANTIALIAS).save(company.profile_picture.path)
        
        return company
