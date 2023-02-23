from django.http import HttpResponseForbidden
from django.test import TestCase, RequestFactory
from django.urls import reverse

from main.tests.test_helpers import (
    PASSWORD,
    create_company_with_admin,
    create_authenticated_user,
    get_company_role,
    create_company_with_logged_in_admin,
    get_company_admin_role,
    get_contact_type,
    create_company,
    get_language,
    get_status,
    create_user,
    get_company_type,
)
from main.decorators import company_role_required
from main.models import (
    User,
    Company,
    CompanyType,
    CompanyUser,
    CompanyRole,
    Contact,
    Address,
    Currency,
    Order,
    OrderType,
)


class DeactivateCompanyTest(TestCase):
    def setUp(self):
        self.company, self.user, _, _ = create_company_with_admin()
        self.order_admin = User.objects.create_user("order_admin", "order_admin@mail.com", PASSWORD)
        CompanyUser.create_order_admin(self.company, self.order_admin)
        self.other_user = User.objects.create_user("other_user", "other_user@mail.com", PASSWORD)

    def test_company_admin_can_deactivate_company(self):
        pass

    def test_order_admin_can_not_deactivate_company(self):
        pass

    def test_non_company_user_can_not_deactivate_company(self):
        pass

    def test_company_admin_of_other_company_can_not_deactivate_company(self):
        pass

    def test_deactivate_button_is_rendered_on_page_for_company_admin(self):
        pass

    def test_deactivate_button_is_not_rendered_on_page_for_order_admin(self):
        pass

    def test_company_status_is_updated_correctly_on_deactivation(self):
        pass


@company_role_required
def i_require_company_admin_role(req, company_id) -> bool:
    if req and company_id:
        pass
    return True


@company_role_required(company_roles=("order_admin",))
def i_require_company_admin_or_order_admin(request, *, company_id) -> bool:
    if request and company_id:
        pass
    return True


class CompanyRoleRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", email="admin@mail.com", password=PASSWORD)
        self.order_admin = User.objects.create_user(
            username="order_admin", email="order_admin@mail.com", password=PASSWORD
        )
        self.company = Company.create("IIsCompany", self.admin_user)
        CompanyUser.create_order_admin(self.company, self.order_admin)
        self.r_factory = RequestFactory()
        self.request = self.r_factory.get(reverse("main:edit_company", args=(self.company.id,)))

    def test_company_admin_can_get_passed_company_role_required(self):
        self._login_user(self.admin_user)
        self.assertTrue(i_require_company_admin_role(self.request, company_id=self.company.id))

    def test_company_admin_can_get_passed_company_admin_or_order_admin_required(self):
        self._login_user(self.admin_user)
        self.assertTrue(i_require_company_admin_or_order_admin(self.request, company_id=self.company.id))

    def test_order_admin_can_get_passed_company_admin_or_order_admin_required(self):
        self._login_user(self.order_admin)
        self.assertTrue(i_require_company_admin_or_order_admin(self.request, company_id=self.company.id))

    def test_order_admin_can_not_get_passed_company_admin_required(self):
        self._login_user(self.order_admin)
        self.assertIsInstance(
            i_require_company_admin_role(self.request, company_id=self.company.id), HttpResponseForbidden
        )

    def _login_user(self, user: User):
        self.client.login(username=user.username, password=PASSWORD)
        self.request.user = user


class EditOrderTest(TestCase):
    def setUp(self):
        self.company, self.user, self.username, self.password = create_company_with_admin(("buyer", "producer"))
        self.order = Order.add(self.company, "Cucumber", 10, "st", Currency.SEK, OrderType.SELL)
        self.url = reverse(
            "main:update_orders",
            args=(self.company.id,),
        )

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
        CompanyUser.create_order_admin(self.company, order_admin)
        self.client.login(username=order_admin.username, password=PASSWORD)
        self.assertRedirects(
            self.client.post(self.url, self._get_post_object(), follow=True),
            reverse("main:edit_company", args=(self.company.id,)),
        )

    def test_non_company_user_can_not_update_order(self):
        user = User.objects.create_user("otheruser", "otheruser@mail.com", PASSWORD)
        self.client.login(username=user.username, password=PASSWORD)
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()).status_code)

    def test_admin_of_other_company_can_not_update_order(self):
        other_admin = User.objects.create_user("otheradmin", "otheradmin@mail.com", PASSWORD)
        Company.create("ShittyCompany", other_admin)
        self.client.login(username=other_admin.username, password=PASSWORD)
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()).status_code)

    def test_order_data_is_updated_correctly(self):
        self.client.login(username=self.username, password=PASSWORD)
        self.client.post(self.url, self._get_post_object("Potato", 5, "kg"))
        order = Order.objects.get(pk=self.order.id)
        self.assertEqual(order.product, "Potato")
        self.assertEqual(order.price_per_unit, 5)
        self.assertEqual(order.unit_type, "kg")

    def _get_post_object(self, product="Cucumber", price_per_unit=10, unit_type="st", currency=Currency.SEK) -> dict:
        return {
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 1,
            "form-0-id": self.order.id,
            "form-0-company": self.company.id,
            "form-0-product": product,
            "form-0-price_per_unit": price_per_unit,
            "form-0-unit_type": unit_type,
            "form-0-currency": currency,
            "form-0-order_type": OrderType.SELL,
        }


class AddOrderContainer:
    def __init__(self, endpoint_name: str, order_type: OrderType):
        (
            self.company,
            self.company_admin,
            self.company_admin_username,
            self.company_admin_password,
        ) = create_company_with_admin(("buyer", "producer"))
        self.url = reverse(endpoint_name, args=(self.company.id,))
        self.order_type = order_type

    def test_non_company_user_can_not_add_order(self, test_case: TestCase):
        create_authenticated_user(test_case.client, "fucker@shitcompany.com")
        test_case.assertEqual(403, test_case.client.post(self.url, self._get_post_data()).status_code)

    def test_order_admin_can_create_order(self, test_case: TestCase):
        user = create_authenticated_user(test_case.client, email="egon@persson.se")
        CompanyUser.objects.create(company=self.company, user=user, role=get_company_role("order_admin"))
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
        company, _ = create_company_with_logged_in_admin(self.client)
        other_user = User.objects.create_user("egon@persson.se", "egon@persson.se", PASSWORD)
        CompanyUser.objects.create(company=company, user=other_user, role=get_company_admin_role())

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
        ) = create_company_with_admin()
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
        company, _ = create_company_with_logged_in_admin(self.client)
        address = Address.objects.create(company=company, address_type="Shit")
        response = self.client.post(reverse("main:delete_address", args=(company.id, address.id)))
        self.assertEqual(response.status_code, 302)


class DeleteContactViewTest(TestCase):
    def test_can_delete_contact(self):
        company, _ = create_company_with_logged_in_admin(self.client)
        contact = Contact.create_contact(company, get_contact_type("email"), "nisse@perssons.se")
        response = self.client.post(reverse("main:delete_contact", args=(company.id, contact.id)))
        self.assertEqual(302, response.status_code)


class AddContactViewTest(TestCase):
    def test_can_add_contact(self):
        company, _ = create_company_with_logged_in_admin(self.client)
        response = self.client.post(
            reverse("main:add_contact", args=(company.id,)),
            {
                "company": company.id,
                "contact_type": get_contact_type("email").id,
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
        create_authenticated_user(self.client)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_valid_post_returns_302(self):
        user = create_authenticated_user(self.client)
        response = self.client.post(self.url, {"name": "Nisse", "user_id": user.id})
        self.assertEqual(302, response.status_code)

    def test_post_redirect(self):
        user = create_authenticated_user(self.client)
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
        company = create_company()
        create_authenticated_user(self.client)

        url = reverse("main:company_profile_picture", args=(company.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)


class EditCompanyViewTest(TestCase):
    def setUp(self):
        self.company, self.admin = create_company_with_logged_in_admin(self.client, ("producer", "buyer"))
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
            self._get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def test_post_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.post(url, self._get_default_post_object()))

    def test_post_can_remove_language(self):
        swe = get_language("SV")
        eng = get_language("EN")
        self.company.content_languages.add(swe, eng)
        self.company.save()

        response = self.client.post(
            self.url,
            self._get_default_post_object(),
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

    @staticmethod
    def _get_default_post_object():
        return {
            "name": "Test Company",
            "company_types": get_company_type("buyer").id,
            "content_languages": get_language("SV").id,
            "external_website_url": "",
        }


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company1 = Company.objects.create(name="test1", status=get_status("active"))
        self.company2 = Company.objects.create(name="test2", status=get_status("active"))
        self.user1 = User.objects.create_user("nissepisse", "nisse@persson.se", PASSWORD)
        self.user2 = User.objects.create_user("egon", "egon@ljung.se", PASSWORD)
        self.user_order_admin = User.objects.create_user("order_admin", "order_admin@mail.com", PASSWORD)
        CompanyUser.objects.create(company=self.company1, user=self.user2, role=get_company_admin_role())
        CompanyUser.objects.create(company=self.company2, user=self.user1, role=get_company_admin_role())
        CompanyUser.create_order_admin(self.company1, self.user_order_admin)

    def test_has_company_role_order_admin(self):
        self.assertTrue(self.company1.has_company_role(self.user_order_admin, CompanyRole.RoleName.order_admin))

    def test_is_company_admin_user_is_admin(self):
        self.assertTrue(self.company1.is_company_admin(self.user2))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(self.company1.is_company_admin(self.user1))

    def test_creator_becomes_admin(self):
        user, _, _ = create_user()
        company = Company.create("Norrlands Bastuklubb", user.id)
        self.assertTrue(company.is_company_admin(user))

    def test_is_producer_on_producer(self):
        company = create_company(["producer"])
        self.assertTrue(company.is_producer())

    def test_is_producer_on_non_producer(self):
        company = create_company(["buyer"])
        self.assertFalse(company.is_producer())

    def test_is_producer_is_case_insensitive(self):
        CompanyType.objects.create(type_name="Producer")
        company = create_company(["Producer"])
        self.assertTrue(company.is_producer())
