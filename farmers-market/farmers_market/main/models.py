from enum import Enum
from typing import Iterable

from django.db.models import (
    Model,
    TextChoices,
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

from .utils import get_localized_value_from_object
from shared.models import Country


class Language(Model):
    iso_639_1 = CharField(max_length=2, unique=True)
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class CompanyType(Model):
    type_name = CharField(max_length=50, unique=True)
    description = CharField(max_length=200)

    class TypeName(Enum):
        PRODUCER = "producer"
        BUYER = "buyer"

    def __str__(self):
        return f"{self.id}: {self.type_name}"


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


class CompanyRole(Model):
    role_name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

    class RoleName(Enum):
        company_admin = "company_admin"
        order_admin = "order_admin"

    @classmethod
    def get(cls, role_name: RoleName) -> "CompanyRole":
        return cls.objects.get(role_name=role_name.value)


class Company(Model):
    name = CharField(max_length=100)
    status = ForeignKey(
        CompanyStatus,
        on_delete=PROTECT,
    )
    created_date = DateTimeField(auto_now_add=True)
    company_types = ManyToManyField(CompanyType, related_name="companies", blank=True)
    content_languages = ManyToManyField(Language, related_name="companies", blank=True)
    activation_date = DateTimeField(null=True, blank=True, default=None)
    external_website_url = CharField(null=True, blank=True, max_length=1000, default=None)
    profile_picture = ImageField(upload_to="company_profile_picture", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"

    def __str__(self):
        return f"{self.id}: {self.name}"

    @classmethod
    def create(cls, name: str, user: User | int) -> "Company":
        """Creates a new company and assigns user as admin."""
        company = cls(name=name, status=CompanyStatus.get(CompanyStatus.StatusName.created))
        company.save()
        CompanyUser.create_company_admin(company, user)
        return company

    @classmethod
    def get(cls, company_id: int, language: str | None = None) -> "Company":
        """
        Get a company by primary key with company description localized.

        pk: Company primary key.

        language: Language to get company description in, if it's available.
        A property on the Company instance named 'description' is set with the translation.

        If language is not provided, this property will be empty.
        """
        if company_id is None:
            raise ValueError("company_id can't be null.")
        try:
            item = cls.objects.get(pk=company_id)
            item.description = item.get_description(language) if language else ""
            return item
        except cls.DoesNotExist:
            raise Exception(f"Company with id {company_id} does not exist")

    @classmethod
    def get_newest(cls, language: str) -> list["Company"]:
        companies = (
            cls.objects.filter(status__status_name__iexact=CompanyStatus.StatusName.active.value)
            .order_by("-activation_date")
            .all()
        )
        for company in companies:
            company.description = company.get_description(language)
        return companies

    def get_description(self, language: str) -> str:
        return get_localized_value_from_object(
            self,
            language,
            "descriptions",
            "description",
            lambda: self.content_languages.all(),
        )

    def is_company_admin(self, user: User | None) -> bool:
        return self.has_company_role(user, ["company_admin"])

    def has_company_role(
        self, user: User | None, roles: list[str | CompanyRole.RoleName] | str | CompanyRole.RoleName | None
    ) -> bool:
        if not user:
            return False
        if isinstance(roles, str):
            roles = [roles]
        if isinstance(roles, CompanyRole.RoleName):
            roles = [roles.value]

        try:
            company_user = self.users.get(user=user)
        except CompanyUser.DoesNotExist:
            return False

        if roles is None:
            return True
        return company_user.role.role_name in roles

    def has_company_type(self, company_type: str) -> bool:
        try:
            self.company_types.get(type_name__iexact=company_type)
        except CompanyType.DoesNotExist:
            return False
        return True

    def is_producer(self) -> bool:
        return self.has_company_type("producer")

    def is_buyer(self) -> bool:
        return self.has_company_type("buyer")

    def is_activated(self) -> bool:
        return self.status.status_name != CompanyStatus.StatusName.created.value

    @property
    def sell_orders(self) -> Iterable["Order"]:
        return self.orders.filter(order_type=OrderType.SELL).all()

    @property
    def buy_orders(self) -> Iterable["Order"]:
        return self.orders.filter(order_type=OrderType.BUY).all()


class CompanyUser(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="users")
    user = ForeignKey(User, on_delete=CASCADE, related_name="companies")
    role = ForeignKey(CompanyRole, on_delete=PROTECT)

    def __str__(self) -> str:
        return f"{self.company.name} - {self.user.email} - {self.role.role_name}"

    @classmethod
    def create_company_user(cls, company, user: User | int | str, role_name: CompanyRole.RoleName) -> "CompanyUser":
        if isinstance(user, (int, str)):
            user = User.objects.get(pk=user)
        user = cls(company=company, user=user, role=CompanyRole.get(role_name))
        user.save()
        return user

    @classmethod
    def create_company_admin(cls, company: Company, user: User | int | str) -> "CompanyUser":
        return cls.create_company_user(company, user, CompanyRole.RoleName.company_admin)

    @classmethod
    def create_order_admin(cls, company: Company, user: User | int | str) -> "CompanyUser":
        return cls.create_company_user(company, user, CompanyRole.RoleName.order_admin)


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

    @classmethod
    def all_for(cls, company: Company) -> Iterable["Address"]:
        return cls.objects.filter(company=company)


class ContactType(Model):
    contact_type = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.contact_type


class Contact(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="contacts")
    contact_type = ForeignKey(ContactType, on_delete=PROTECT)
    value = CharField(max_length=500)
    description = CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.value} - {self.contact_type.contact_type}"

    @classmethod
    def create_contact(
        cls, company: Company, contact_type: ContactType, value: str, description: str = None
    ) -> "Contact":
        return cls.objects.create(
            company=company,
            contact_type=contact_type,
            value=value,
            description=description,
        )

    @classmethod
    def all_for(cls, company: Company) -> Iterable["Contact"]:
        return cls.objects.filter(company=company)


class Currency(TextChoices):
    SEK = "SEK", _("SEK")


class OrderType(TextChoices):
    SELL = "sell", _("Sell order")
    BUY = "buy", _("Buy order")


class Order(Model):
    company = ForeignKey(Company, on_delete=CASCADE, related_name="orders")
    product = CharField(max_length=200)
    price_per_unit = DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unit_type = CharField(max_length=20, null=True, blank=True)
    currency = CharField(max_length=3, choices=Currency.choices)
    order_type = CharField(max_length=10, choices=OrderType.choices)

    def __str__(self):
        return f"{self.company.name}: {self.product}"

    @classmethod
    def add(
        cls,
        company: Company,
        product: str,
        price_per_unit: float | None,
        unit_type: str | None,
        currency: Currency,
        order_type: OrderType,
    ) -> "Order":
        return cls.objects.create(
            company=company,
            product=product,
            price_per_unit=price_per_unit,
            unit_type=unit_type,
            currency=currency,
            order_type=order_type,
        )
