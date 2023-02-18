from typing import Iterable

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
    Currency,
    Order,
    OrderType,
)

PASSWORD = "test123"


class EditOrderTest(TestCase):
    def setUp(self):
        self.company, self.user, self.username, self.password = _create_company_with_admin(("buyer", "producer"))
        self.order = Order.add(self.company, "Cucumber", 10, "st", Currency.SEK, OrderType.SELL)
        self.url = reverse("main:update_order", args=(self.order.id,))

    def test_can_not_call_with_get(self):
        self.assertEqual(404, self.client.get(self.url).status_code)

    def test_admin_can_update_order(self):
        self.client.login(username=self.username, password=self.password)
        self.assertRedirects(
            self.client.post(self.url, self._get_post_object(), follow=True),
            reverse("main:edit_company", args=(self.company.id,)),
        )

    def test_order_admin_can_update_order(self):
        order_admin = User.objects.create_user("IAdminOrders@gmail.com", "IAdminOrders@gmail.com", PASSWORD)
        CompanyUser.create_order_admin(self.company, order_admin.id)
        self.client.login(username=order_admin.username, password=PASSWORD)
        self.assertRedirects(
            self.client.post(self.url, self._get_post_object(), follow=True),
            reverse("main:edit_company", args=(self.company.id,)),
        )

    def test_non_company_user_can_not_update_order(self):
        user = User.objects.create_user("otheruser", "otheruser@mail.com", PASSWORD)
        self.client.login(username=user.username, password=PASSWORD)
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()))

    def test_admin_of_other_company_can_not_update_order(self):
        other_admin = User.objects.create_user("otheradmin", "otheradmin@mail.com", PASSWORD)
        Company.create("ShittyCompany", other_admin)
        self.client.login(username=other_admin.username, password=PASSWORD)
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()))

    def test_order_data_is_updated_correctly(self):
        self.client.login(username=self.username, password=PASSWORD)
        self.client.post(self.url, self._get_post_object("Potato", 5, "kg"))
        order = Order.objects.get(pk=self.order.id)
        self.assertEqual(order.product, "Potato")
        self.assertEqual(order.price_per_unit, 5)
        self.assertEqual(order.unit_type, "kg")

    def _get_post_object(self, product="Cucumber", price_per_unit=10, unit_type="st", currency=Currency.SEK) -> dict:
        return {
            "company": self.company.id,
            "product": product,
            "price_per_unit": price_per_unit,
            "unit_type": unit_type,
            "currency": currency,
            "order_type": OrderType.SELL,
        }


class AddOrderContainer:
    def __init__(self, endpoint_name: str, order_type: OrderType):
        (
            self.company,
            self.company_admin,
            self.company_admin_username,
            self.company_admin_password,
        ) = _create_company_with_admin(("buyer", "producer"))
        self.url = reverse(endpoint_name, args=(self.company.id,))
        self.order_type = order_type

    def test_non_company_user_can_not_add_order(self, test_case: TestCase):
        _create_authenticated_user(test_case.client, "fucker@shitcompany.com")
        test_case.assertEqual(403, test_case.client.post(self.url, self._get_post_data()).status_code)

    def test_order_admin_can_create_order(self, test_case: TestCase):
        user = _create_authenticated_user(test_case.client, email="egon@persson.se")
        CompanyUser.objects.create(company=self.company, user=user, role=_get_company_role("order_admin"))
        response = test_case.client.post(self.url, self._get_post_data())
        test_case.assertEqual(302, response.status_code)

    def test_order_is_added_correctly(self, test_case: TestCase):
        test_case.client.login(username=self.company_admin_username, password=self.company_admin_password)
        test_case.client.post(self.url, self._get_post_data())
        self._verify_sell_order(test_case)

    def _verify_sell_order(self, test_case: TestCase):
        order = Order.objects.get(company=self.company, product="cucumber")
        test_case.assertEqual(100.50, order.price_per_unit)
        test_case.assertEqual("kg", order.unit_type)
        test_case.assertEqual(Currency.SEK, order.currency)
        test_case.assertEqual(self.order_type, order.order_type)

    def _get_post_data(self):
        return {
            "company": self.company.id,
            "product": "cucumber",
            "price_per_unit": 100.50,
            "unit_type": "kg",
            "currency": Currency.SEK,
            "order_type": self.order_type,
        }


class AddBuyOrderTest(TestCase):
    def setUp(self):
        self.container = AddOrderContainer("main:add_buy_order", OrderType.BUY)

    def test_non_company_user_can_not_add_buy_order(self):
        self.container.test_non_company_user_can_not_add_order(self)

    def test_order_admin_can_create_buy_order(self):
        self.container.test_order_admin_can_create_order(self)

    def test_buy_order_is_added_correctly(self):
        self.container.test_order_is_added_correctly(self)


class AddSellOrderTest(TestCase):
    def setUp(self):
        self.container = AddOrderContainer("main:add_sell_order", OrderType.SELL)

    def test_company_admin_can_create_sell_order(self):
        self.container.test_non_company_user_can_not_add_order(self)

    def test_order_admin_can_create_sell_order(self):
        self.container.test_order_admin_can_create_order(self)

    def test_sell_order_is_added_correctly(self):
        self.container.test_order_is_added_correctly(self)


class CompanyUsersViewTest(TestCase):
    def test_can_delete_user(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        other_user = User.objects.create_user("egon@persson.se", "egon@persson.se", PASSWORD)
        CompanyUser.objects.create(company=company, user=other_user, role=_get_company_admin_role())

        response = self.client.post(reverse("main:delete_company_user", args=(company.id, other_user.id)), follow=True)

        try:
            CompanyUser.objects.get(company=company, user=other_user)
        except CompanyUser.DoesNotExist:
            pass
        else:
            self.fail("CompanyUser not removed")

        self.assertRedirects(
            response,
            expected_url=reverse("main:company_users", args=(company.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )


class ActivateCompanyViewTest(TestCase):
    def setUp(self):
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
        User.objects.create_user(username, username, PASSWORD)
        self.client.login(username=username, password=PASSWORD)
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_superuser_can_activate(self):
        username = "superuser@test.se"
        User.objects.create_superuser(username, username, PASSWORD)
        self.client.login(username=username, password=PASSWORD)
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
    def test_can_delete_address(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        address = Address.objects.create(company=company, address_type="Shit")
        response = self.client.post(reverse("main:delete_address", args=(company.id, address.id)))
        self.assertEqual(response.status_code, 302)


class DeleteContactViewTest(TestCase):
    def test_can_delete_contact(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        contact = Contact.create_contact(company, _get_contact_type("email"), "nisse@perssons.se")
        response = self.client.post(reverse("main:delete_contact", args=(company.id, contact.id)))
        self.assertEqual(302, response.status_code)


class AddContactViewTest(TestCase):
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
    def test_non_company_admin_can_not_post_to_view(self):
        company = _create_company()
        _create_authenticated_user(self.client)

        url = reverse("main:company_profile_picture", args=(company.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)


class EditCompanyViewTest(TestCase):
    def setUp(self):
        self.company, self.admin = _create_company_with_logged_in_admin(self.client, ("producer", "buyer"))
        self.url = reverse("main:edit_company", args=(self.company.id,))

    def test_sell_orders_are_returned_in_response(self):
        order = Order.add(self.company, "Cucumber", 5, "kg", Currency.SEK, OrderType.SELL)
        response = self.client.get(self.url)
        self.assertEqual(list(response.context.get("sell_orders")), [order])

    def test_get_returns_200(self):
        self.assertEquals(self.client.get(self.url).status_code, 200)

    def test_get_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.get(url))

    def test_post_returns_202(self):
        response = self.client.post(
            self.url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def test_post_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.post(url, _get_default_post_object()))

    def test_post_can_remove_language(self):
        swe = _get_language("SV")
        eng = _get_language("EN")
        self.company.content_languages.add(swe, eng)
        self.company.save()

        response = self.client.post(
            self.url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def test_producer_has_add_sell_order_form(self):
        self.company.company_types.get(type_name="buyer").delete()
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context.get("add_sell_order_form"))
        self.assertTrue(response.context.get("is_producer"))

    def test_buyer_has_add_buy_order_form(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context.get("add_buy_order_form"))
        self.assertTrue(response.context.get("is_buyer"))

    def test_company_with_producer_and_buyer_has_add_sell_order_form(self):
        response = self.client.get(self.url)
        self.assertIsNotNone(response.context.get("add_sell_order_form"))
        self.assertTrue(response.context.get("is_producer"))

    def _method_requires_company_admin(self, func):
        user = User.objects.create_user("nisse", "nisse@pisse.se", PASSWORD)
        self.client.login(username=user.username, password=PASSWORD)
        self.assertEquals(func(self.url).status_code, 403)


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company1 = Company.objects.create(name="test1", status=_get_status("active"))
        self.company2 = Company.objects.create(name="test2", status=_get_status("active"))
        self.user1 = User.objects.create_user("nissepisse", "nisse@persson.se", PASSWORD)
        self.user2 = User.objects.create_user("egon", "egon@ljung.se", PASSWORD)
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

    def test_is_producer_on_producer(self):
        company = _create_company(["producer"])
        self.assertTrue(company.is_producer())

    def test_is_producer_on_non_producer(self):
        company = _create_company(["buyer"])
        self.assertFalse(company.is_producer())

    def test_is_producer_is_case_insensitive(self):
        CompanyType.objects.create(type_name="Producer")
        company = _create_company(["Producer"])
        self.assertTrue(company.is_producer())


def _get_default_post_object():
    return {
        "name": "Test Company",
        "company_types": _get_company_type("buyer").id,
        "content_languages": _get_language("SV").id,
        "external_website_url": "",
    }


def _create_user(email="nisse@persson.se", password=PASSWORD) -> tuple[User, str, str]:
    user = User.objects.create_user(email, email, password)
    user.save()
    return user, email, password


def _create_authenticated_user(client: Client, email="nisse@persson.se", password=PASSWORD) -> User:
    user, username, password = _create_user(email=email, password=password)
    client.login(username=username, password=password)
    return user


def _create_company_with_admin(company_types: Iterable[str] = ()) -> tuple[Company, User, str, str]:
    """
    Creates a company with an admin user.

    Returns:
        Tuple[Company, User, username, password]
    """
    company = _create_company(company_types=company_types)
    role = _get_company_admin_role()
    user, username, password = _create_user()
    CompanyUser.objects.create(company=company, role=role, user=user)
    return company, user, username, password


def _create_company_with_logged_in_admin(client: Client, company_types: Iterable[str] = ()) -> tuple[Company, User]:
    company, user, username, password = _create_company_with_admin(company_types=company_types)
    client.login(username=username, password=password)
    return company, user


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


def _create_company(company_types: Iterable[str] = ()) -> Company:
    company = Company.objects.create(name="Nisses firma", status=_get_status("active"))
    for company_type in company_types:
        company.company_types.add(_get_company_type(company_type))
    return company


def _get_contact_type(contact_type) -> ContactType:
    return ContactType.objects.get(contact_type=contact_type)
