from django.test import TestCase, Client
from django.urls import reverse

from .models import (
    User,
    Company,
    Language,
    CompanyType,
    CompanyUser,
    CompanyRole,
    CompanyStatus,
    ContactType,
    Contact,
    Address,
    Product,
    Currency,
    Order,
    OrderType,
)


class AddSellOrderTest(TestCase):
    def setUp(self):
        _setup_defaults()
        (
            self.company,
            self.company_admin,
            self.company_admin_username,
            self.company_admin_password,
        ) = _create_company_with_admin()
        self.url = reverse("main:add_sell_order", args=(self.company.id,))
        self.product = _create_product("cucumber")

    def test_non_company_user_can_not_add_sell_order(self):
        _create_authenticated_user(self.client, email="fucker@shitcompany.com")
        response = self.client.post(
            self.url,
            self._get_post_data(),
        )
        self.assertEqual(403, response.status_code)

    def test_company_admin_can_create_sell_order(self):
        self.client.login(username=self.company_admin_username, password=self.company_admin_password)
        response = self.client.post(self.url, self._get_post_data())
        self.assertEqual(302, response.status_code)

    def test_order_admin_can_create_sell_order(self):
        user = _create_authenticated_user(self.client, email="egon@persson.se")
        CompanyUser.objects.create(company=self.company, user=user, role=_get_company_role("order_admin"))
        response = self.client.post(self.url, self._get_post_data())
        self.assertEqual(302, response.status_code)

    def test_sell_order_is_added_correctly(self):
        self.client.login(username=self.company_admin_username, password=self.company_admin_password)
        self.client.post(self.url, self._get_post_data())
        self._verify_sell_order()

    def _verify_sell_order(self):
        order = Order.objects.get(company=self.company, product=self.product)
        self.assertEqual(100.50, order.price_per_unit)
        self.assertEqual("kg", order.unit_type)
        self.assertEqual(_get_currency("SEK"), order.currency)
        self.assertEqual(OrderType.SELL, order.order_type)

    def _get_post_data(self):
        return {
            "company": self.company.id,
            "product": self.product.id,
            "price_per_unit": 100.50,
            "unit_type": "kg",
            "currency": _get_currency("SEK").id,
            "order_type": "sell",
        }


class CompanyUsersViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_can_delete_user(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        other_user = User.objects.create_user("egon@persson.se", "egon@persson.se", "test123")
        CompanyUser.objects.create(company=company, user=other_user, role=_get_company_admin_role())

        response = self.client.post(reverse("main:delete_company_user", args=(company.id, other_user.id)), follow=True)

        with self.assertRaises(CompanyUser.DoesNotExist):
            CompanyUser.objects.get(company=company, user=other_user)
        self.assertRedirects(
            response,
            expected_url=reverse("main:company_users", args=(company.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )


class ActivateCompanyViewTest(TestCase):
    def setUp(self):
        _setup_defaults()
        (
            self.company_with_admin,
            self.company_admin_user,
            self.admin_user_username,
            self.admin_user_password,
        ) = _create_company_with_admin()
        self.url = reverse("main:activate_company", args=(self.company_with_admin.id,))

    def test_http_get_returns_404(self):
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_successfull_activation_returns_302(self):
        self.client.login(username=self.admin_user_username, password=self.admin_user_password)
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_non_admin_user_returns_403(self):
        username = "nonadmin@test.se"
        password = "test123"
        User.objects.create_user(username, username, password)
        self.client.login(username=username, password=password)
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_superuser_can_activate(self):
        username = "superuser@test.se"
        password = "test123"
        User.objects.create_superuser(username, username, password)
        self.client.login(username=username, password=password)
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_success_redirects_back_to_edit_company_view(self):
        self.client.login(username=self.admin_user_username, password=self.admin_user_password)
        self.assertRedirects(
            self.client.post(self.url, follow=True),
            reverse("main:edit_company", args=(self.company_with_admin.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )


class DeleteAddressViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_can_delete_address(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        address = Address.objects.create(company=company, address_type="Shit")
        response = self.client.post(reverse("main:delete_address", args=(company.id, address.id)))
        self.assertEqual(response.status_code, 302)


class DeleteContactViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_can_delete_contact(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        contact = Contact.create_contact(company, _get_contact_type("email"), "nisse@perssons.se")
        response = self.client.post(reverse("main:delete_contact", args=(company.id, contact.id)))
        self.assertEqual(302, response.status_code)


class AddContactViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_can_add_contact(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        response = self.client.post(
            reverse("main:add_contact", args=(company.id,)),
            {
                "company": company.id,
                "contact_type": _get_contact_type("email").id,
                "value": "nisse@perssons.se",
                "description": "Boss",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        contact = Contact.objects.get(value="nisse@perssons.se")
        self.assertEqual(contact.company.name, company.name)
        self.assertEqual(contact.description, "Boss")


class NewCompanyViewTest(TestCase):
    url = reverse("main:new_company")

    def setUp(self):
        _setup_defaults()

    def test_get_returns_200(self):
        _create_authenticated_user(self.client)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_valid_post_returns_302(self):
        user = _create_authenticated_user(self.client)
        response = self.client.post(self.url, {"name": "Nisse", "user_id": user.id})
        self.assertEqual(302, response.status_code)

    def test_post_redirect(self):
        user = _create_authenticated_user(self.client)
        response = self.client.post(self.url, {"name": "TestCompany", "user_id": user.id}, follow=True)
        company = Company.objects.get(name="TestCompany")
        self.assertRedirects(
            response,
            reverse("main:edit_company", args=(company.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )


class CompanyProfilePictureViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_non_company_admin_can_not_post_to_view(self):
        company = _create_company()
        _create_authenticated_user(self.client)

        url = reverse("main:company_profile_picture", args=(company.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)


class EditCompanyViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_get_returns_200(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.get(url))

    def test_post_returns_202(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.post(
            url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def test_post_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.post(url, _get_default_post_object()))

    def test_post_can_remove_language(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        swe = _get_language("SV")
        eng = _get_language("EN")
        company.content_languages.add(swe, eng)
        company.save()

        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.post(
            url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def _method_requires_company_admin(self, func):
        company = _create_company()
        _create_authenticated_user(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = func(url)
        self.assertEquals(response.status_code, 403)


class CompanyModelTest(TestCase):
    def setUp(self):
        _setup_defaults()
        self.company1 = Company.objects.create(name="test1", status=_get_status("active"))
        self.company2 = Company.objects.create(name="test2", status=_get_status("active"))
        self.user1 = User.objects.create_user("nissepisse", "nisse@persson.se", "test123")
        self.user2 = User.objects.create_user("egon", "egon@ljung.se", "test123")
        CompanyUser.objects.create(company=self.company1, user=self.user2, role=_get_company_admin_role())
        CompanyUser.objects.create(company=self.company2, user=self.user1, role=_get_company_admin_role())

    def test_is_company_admin_user_is_admin(self):
        self.assertTrue(self.company1.is_company_admin(self.user2))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(self.company1.is_company_admin(self.user1))

    def test_creator_becomes_admin(self):
        user, _, _ = _create_user()
        company = Company.create("Norrlands Bastuklubb", user.id)
        self.assertTrue(company.is_company_admin(user))


def _get_default_post_object():
    return {
        "name": "Test Company",
        "company_types": _get_company_type("buyer").id,
        "content_languages": _get_language("SV").id,
        "external_website_url": "",
    }


def _create_user(email="nisse@persson.se", password="test123") -> tuple[User, str, str]:
    user = User.objects.create_user(email, email, password)
    user.save()
    return user, email, password


def _create_authenticated_user(client: Client, email="nisse@persson.se", password="test123") -> User:
    user, username, password = _create_user(email=email, password=password)
    client.login(username=username, password=password)
    return user


def _create_company_with_admin() -> tuple[Company, User, str, str]:
    company = _create_company()
    role = _get_company_admin_role()
    user, username, password = _create_user()
    CompanyUser.objects.create(company=company, role=role, user=user)
    return company, user, username, password


def _create_company_with_logged_in_admin(client: Client) -> tuple[Company, User]:
    company, user, username, password = _create_company_with_admin()
    client.login(username=username, password=password)
    return company, user


def _create_product(code: str) -> Product:
    return Product.objects.create(product_code=code)


def _get_company_admin_role() -> CompanyRole:
    return _get_company_role("company_admin")


def _get_company_role(role_name: str) -> CompanyRole:
    return CompanyRole.objects.get(role_name=role_name)


def _get_company_type(type_name: str) -> CompanyType:
    return CompanyType.objects.get(type_name=type_name)


def _get_language(iso_639_1):
    return Language.objects.get(iso_639_1=iso_639_1)


def _get_status(status_name):
    return CompanyStatus.objects.get(status_name=status_name)


def _create_company() -> Company:
    company = Company.objects.create(name="Nisses firma", status=_get_status("active"))
    company.company_types.add(_get_company_type("producer"))
    return company


def _get_contact_type(contact_type) -> ContactType:
    return ContactType.objects.get(contact_type=contact_type)


def _get_currency(currency_code: str) -> Currency:
    return Currency.objects.get(currency_code=currency_code)


def _setup_defaults():
    CompanyRole.objects.create(role_name="company_admin")
    CompanyRole.objects.create(role_name="order_admin")
    CompanyStatus.objects.create(status_name="created")
    CompanyStatus.objects.create(status_name="active")
    Language.objects.create(iso_639_1="SV")
    Language.objects.create(iso_639_1="EN")
    CompanyType.objects.create(type_name="producer")
    CompanyType.objects.create(type_name="buyer")
    ContactType.objects.create(contact_type="email")
    ContactType.objects.create(contact_type="phone")
    Currency.objects.create(currency_code="SEK")
