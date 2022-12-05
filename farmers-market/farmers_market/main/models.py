from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Language(models.Model):
    iso_639_1 = models.CharField(max_length=2)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.iso_639_1}: {self.name}"


class CompanyType(models.Model):
    type_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.type_name


class CompanyStatus(models.Model):
    status_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name


class ChangeType(models.Model):
    change_type = models.CharField(max_length=20)

    def __str__(self):
        return self.change_type


class Company(models.Model):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(CompanyStatus, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    company_types = models.ManyToManyField(CompanyType, related_name="companies")
    content_languages = models.ManyToManyField(Language, related_name="companies")
    activation_date = models.DateTimeField(null=True, blank=True, default=None)
    external_website_url = models.CharField(null=True, blank=True, max_length=1000)
    profile_picture_url = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.name
    
    def get_description(self, language: str) -> str:
        if len(language) > 2:
            language = language[:2].upper()
        descriptions = self.descriptions.all()
        description = self._get_description(language, descriptions)
        if not description:
            for content_language in self.content_languages:
                description = self._get_description(content_language.iso_639_1.upper(), descriptions)
                if description:
                    break
        return description or next(iter(d.description for d in descriptions), "")
    
    def is_company_admin(self, user: User | None) -> bool:
        if not user:
            return False
        
    
    def _get_description(self, language: str, descriptions) -> str:
        description = next(iter(d for d in descriptions if d.language.iso_639_1.upper() == language), None)
        if description:
            return description.description
        return None


class CompanyRole(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class CompanyUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(CompanyRole, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.company.name} - {self.user.email} - {self.role.role_name}"


class CompanyChange(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    change_type = models.ForeignKey(ChangeType, on_delete=models.PROTECT)
    field = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed = models.DateTimeField(auto_now_add=True)
    new_value = models.TextField()

    def __str__(self):
        return f"{self.change_type.change_type} - {self.field} - {self.new_value}"

class CompanyDescription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="descriptions")
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="company_descriptions")
    description = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.company.name} - {_(self.language.name)}"


class Country(models.Model):
    country_iso_3166_1 = models.CharField(max_length=2)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.country_iso_3166_1} - {_(self.name)}"


class Address(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(max_length=50, null=True, blank=True)
    addressee = models.CharField(max_length=100, null=True, blank=True)
    co_address = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.company.name} - {self.address_type} - {self.street_address}"


class ContactType(models.Model):
    contact_type = models.CharField(max_length=100)

    def __str__(self):
        return self.contact_type


class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_type = models.ForeignKey(ContactType, on_delete=models.PROTECT)
    value = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.contact_type.contact_type}"


class Product(models.Model):
    product_code = models.CharField(max_length=50)

    def __str__(self):
        return self.product_code


class ProductName(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product.product_code} - {self.language.name} - {self.name}"


class Currency(models.Model):
    currency_code = models.CharField(max_length=3)

    def __str__(self):
        return self.currency_code


class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    unit_type = models.CharField(max_length=20, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.company.name} - {self.product.product_code}"
