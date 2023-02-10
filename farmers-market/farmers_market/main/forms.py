from typing import Mapping, Any

from django.db.utils import ProgrammingError
from django.forms import (
    ModelForm,
    Form,
    CharField,
    Textarea,
    ChoiceField,
    ModelMultipleChoiceField,
    ModelChoiceField,
    CheckboxSelectMultiple,
    RadioSelect,
    HiddenInput,
    TextInput,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shared.forms import UploadCroppedPictureModelForm
from .fields import ForeignKeyRefField, UserField
from .models import (
    Company,
    CompanyType,
    Language,
    Contact,
    ContactType,
    Address,
    Country,
    CompanyDescription,
    CompanyUser,
    CompanyRole,
    Order,
    Currency,
    OrderType,
)


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


class UploadCompanyProfilePictureForm(UploadCroppedPictureModelForm):
    def __init__(self, instance: Company, data: Mapping = None, files: Mapping = None, *args, **kwargs):
        super().__init__(
            reverse("main:company_profile_picture", args=(instance.id,)), instance, data, files, *args, **kwargs
        )

    class Meta(UploadCroppedPictureModelForm.Meta):
        model = Company


class AddCompanyUserForm(ModelForm):
    user = UserField()
    company = ForeignKeyRefField(Company)
    try:
        role = ModelChoiceField(CompanyRole.objects.all(), initial=CompanyRole.objects.get())
    except CompanyRole.DoesNotExist:
        role = ModelChoiceField(CompanyRole.objects.all())
    except ProgrammingError:
        role = ChoiceField()

    class Meta:
        model = CompanyUser
        fields = ["user", "company", "role"]

    def __init__(self, company: Company, data: Mapping | None = None):
        super().__init__(instance=CompanyUser(company=company), data=data)

    def save(self, **kwargs) -> CompanyUser:
        return CompanyUser.objects.create(
            user=self.cleaned_data["user"], company=self.cleaned_data["company"], role=self.cleaned_data["role"]
        )


class AddSellOrderForm(ModelForm):
    company = ForeignKeyRefField(Company)
    order_type = CharField(initial=OrderType.SELL, widget=HiddenInput)
    currency = ChoiceField(choices=Currency.choices, initial=Currency.SEK, widget=RadioSelect)

    def __init__(self, company: Company, data: Mapping[str, Any] = None):
        super().__init__(data=data)
        self.fields["company"].initial = company.id

    class Meta:
        model = Order
        fields = ["company", "product", "price_per_unit", "unit_type", "currency", "order_type"]
