from enum import Enum

from django.db.models import (
    Model,
    CharField,
    DateTimeField,
    TextField,
    DecimalField,
    ImageField,
    ManyToManyField,
    ForeignKey,
    PROTECT,
    CASCADE,
    SET_NULL,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Language(Model):
    iso_639_1 = CharField(max_length=2, unique=True)
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.iso_639_1}: {self.name}"


class CompanyType(Model):
    type_name = CharField(max_length=50, unique=True)
    description = CharField(max_length=200)

    def __str__(self):
        return f"Name: {self.type_name}"


class CompanyStatus(Model):
    status_name = CharField(max_length=50, unique=True)
    description = CharField(max_length=200)

    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name = "Company Status"
        verbose_name_plural = "Company Statuses"

    class StatusName(Enum):
        created = "created"
        active = "active"
        deactivated = "deactivated"

    @classmethod
    def get(cls, status_name: StatusName) -> "CompanyStatus":
        try:
            status = cls.objects.get(status_name=status_name.value)
        except cls.DoesNotExist:
            status = cls.objects.create(status_name=status_name.value, description="AutoAdded")
        return status


class ChangeType(Model):
    change_type = CharField(max_length=20)

    def __str__(self):
        return self.change_type


class Company(Model):
    name = CharField(max_length=100)
    status = ForeignKey(
        CompanyStatus, on_delete=PROTECT,
    )
    created_date = DateTimeField(auto_now_add=True)
    company_types = ManyToManyField(CompanyType, related_name="companies")
    content_languages = ManyToManyField(Language, related_name="companies")
    activation_date = DateTimeField(null=True, blank=True, default=None)
    external_website_url = CharField(null=True, blank=True, max_length=1000, default=None)
    profile_picture = ImageField(upload_to="company_profile_picture", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"

    def __str__(self):
        return f"{self.id}: {self.name}"

    @classmethod
    def create(cls, name: str, user_id: int) -> "Company":
        """Creates a new company and assigns user as admin."""
        company = cls(
            name=name,
            status=CompanyStatus.get(CompanyStatus.StatusName.created)
        )
        company.save()
        CompanyUser.create_company_admin(company, user_id)
        return company

    @classmethod
    def get(cls, pk: int, language: str) -> "Company":
        """Get a company by primary key with company description localized."""
        item = cls.objects.get(pk=pk)
        item.description = item.get_description(language)
        return item

    @classmethod
    def get_newest(language: str) -> list["Company"]:
        pass

    def get_description(self, language: str) -> str:
        if len(language) > 2:
            language = language[:2].upper()
        descriptions = self.descriptions.all()
        description = self._get_description(language, descriptions)
        if not description:
            for content_language in self.content_languages.all():
                description = self._get_description(content_language.iso_639_1.upper(), descriptions)
                if description:
                    break
        return description or next(iter(d.description for d in descriptions), "")

    def is_company_admin(self, user: User | None) -> bool:
        if not user:
            return False
        try:
            self.users.get(pk=user.id)
        except CompanyUser.DoesNotExist:
            return False
        return True

    def _get_description(self, language: str, descriptions) -> str:
        description = next(iter(d for d in descriptions if d.language.iso_639_1.upper() == language), None)
        if description:
            return description.description
        return None


class CompanyRole(Model):
    role_name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name
    
    class RoleName(Enum):
        company_admin = "company_admin"
    
    @classmethod
    def get(cls, role_name: RoleName) -> "CompanyRole":
        return cls.objects.get(role_name=role_name.value)


class CompanyUser(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="users")
    user = ForeignKey(User, on_delete=CASCADE)
    role = ForeignKey(CompanyRole, on_delete=PROTECT)

    def __str__(self) -> str:
        return f"{self.company.name} - {self.user.email} - {self.role.role_name}"
    
    @classmethod
    def create_company_admin(cls, company: Company, user_id: int) -> "CompanyUser":
        user = cls(company=company, user=User.objects.get(pk=user_id), role=CompanyRole.get(CompanyRole.RoleName.company_admin))
        user.save()
        return user


class CompanyChange(Model):
    company = ForeignKey(Company, on_delete=CASCADE)
    change_type = ForeignKey(ChangeType, on_delete=PROTECT)
    field = CharField(max_length=50)
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    changed = DateTimeField(auto_now_add=True)
    new_value = TextField()

    def __str__(self):
        return f"{self.change_type.change_type} - {self.field} - {self.new_value}"


class CompanyDescription(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="descriptions")
    language = ForeignKey(Language, on_delete=PROTECT, related_name="company_descriptions")
    description = CharField(max_length=2000)

    def __str__(self):
        return f"{self.company.name} - {_(self.language.name)}"


class Country(Model):
    country_iso_3166_1 = CharField(max_length=2, unique=True)
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.country_iso_3166_1} - {_(self.name)}"
    
    class Meta:
        verbose_name_plural = "Countries"


class Address(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="addresses")
    address_type = CharField(max_length=50, null=True, blank=True)
    addressee = CharField(max_length=100, null=True, blank=True)
    co_address = CharField(max_length=100, null=True, blank=True)
    street_address = CharField(max_length=100, null=True, blank=True)
    city = CharField(max_length=20, null=True, blank=True)
    zip_code = CharField(max_length=10, null=True, blank=True)
    country = ForeignKey(Country, on_delete=PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} - {self.address_type} - {self.street_address}"
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class ContactType(Model):
    contact_type = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.contact_type


class Contact(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="contacts")
    contact_type = ForeignKey(ContactType, on_delete=PROTECT)
    value = CharField(max_length=500)
    description = CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.contact_type.contact_type}"


class Product(Model):
    product_code = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.product_code


class ProductName(Model):
    product = ForeignKey(Product, on_delete=PROTECT)
    language = ForeignKey(Language, on_delete=PROTECT)
    name = CharField(max_length=200)

    def __str__(self):
        return f"{self.product.product_code} - {self.language.name} - {self.name}"


class Currency(Model):
    currency_code = CharField(max_length=3, unique=True)

    def __str__(self):
        return self.currency_code
    
    class Meta:
        verbose_name_plural = "Currencies"


class Order(Model):
    company = ForeignKey(Company, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=PROTECT)
    price_per_unit = DecimalField(max_digits=20, decimal_places=2, null=True)
    unit_type = CharField(max_length=20, null=True)
    currency = ForeignKey(Currency, on_delete=PROTECT)

    def __str__(self):
        return f"{self.company.name} - {self.product.product_code}"
