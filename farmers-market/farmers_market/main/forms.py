from django.forms import (
    ModelForm,
    Form,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
    FileField,
    FloatField,
    CharField,
    HiddenInput,
    FileInput,
    TextInput,
    
)
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import Company, CompanyType, Language, Contact


class AddContactForm(ModelForm):
    company = 

    class Meta:
        model = Contact
        fields = ["company", "contact_type", "value", "description"]


class NewCompanyForm(Form):
    name = CharField(
        max_length=255,
        #  forms ↓
        widget=TextInput(attrs={"autofocus": True}),
    )
    user_id = CharField(widget=HiddenInput)

    class Meta:
        fields = ["name"]

    def save(self):
        return Company.create(self.cleaned_data.get("name"), self.cleaned_data.get("user_id"))


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
    profile_picture = FileField(required=True, label=_("upload_profile_picture_label"), widget=FileInput)

    class Meta:
        model = Company
        fields = ["profile_picture", "x", "y", "width", "height"]

    def save(self):
        company: Company = super().save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        Image.open(company.profile_picture).crop((x, y, x + width, y + height)).resize((300, 300), Image.ANTIALIAS).save(
            company.profile_picture.path
        )

        return company
