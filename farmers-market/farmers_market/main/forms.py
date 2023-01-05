from typing import Mapping, Any

from django.forms import (
    ModelForm,
    Form,
    ModelMultipleChoiceField,
    ModelChoiceField,
    CheckboxSelectMultiple,
    RadioSelect,
    FileField,
    FloatField,
    CharField,
    HiddenInput,
    FileInput,
    TextInput,
    Textarea,
)
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import Company, CompanyType, Language, Contact, ContactType, Address, Country, CompanyDescription
from .fields import ForeignKeyRefField


class AddressForm(ModelForm):
    company = ForeignKeyRefField(Company)
    country = ModelChoiceField(Country.objects.all(), widget=RadioSelect, required=False)

    class Meta:
        model = Address
        fields = ["company", "address_type", "addressee", "co_address", "street_address", "city", "zip_code", "country"]


class ContactForm(ModelForm):
    company = ForeignKeyRefField(Company)
    contact_type = ModelChoiceField(ContactType.objects.all(), widget=RadioSelect, required=True)

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

    def __init__(self, *args, instance: Company, data: Mapping[str, Any] = None, **kwargs):
        super().__init__(data, *args, instance=instance, **kwargs)
        languages = instance.content_languages.all()
        for language in languages:
            try:
                desc = instance.descriptions.get(language=language)
            except CompanyDescription.DoesNotExist:
                desc = CompanyDescription(company=instance, language=language)
            self.fields[f"desc_{language.iso_639_1}"] = CharField(
                required=False,
                widget=Textarea(attrs={"rows": 5}),
                initial=desc.description,
                label=_(f"Description {language.name}"),
            )

    class Meta:
        model = Company
        fields = ["name", "company_types", "content_languages", "external_website_url"]

    def save(self, commit: bool = ...) -> Any:
        company = super().save(commit)
        languages = company.content_languages.all()
        for language in languages:
            try:
                cleaned_desc = self.cleaned_data[f"desc_{language.iso_639_1}"]
            except KeyError:
                pass
            else:
                if cleaned_desc:
                    try:
                        desc = company.descriptions.get(language=language)
                    except CompanyDescription.DoesNotExist:
                        desc = CompanyDescription(company=company, language=language)
                    desc.description = cleaned_desc
                    desc.save()
        company.descriptions.exclude(language__in=languages).delete()
        return company


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
