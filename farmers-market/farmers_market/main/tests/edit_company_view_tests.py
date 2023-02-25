from django.urls import reverse

from .test_helpers import TestCase, create_company_with_logged_in_admin, get_language, create_user, get_company_type
from ..models import Currency, OrderType, Order


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
        user = create_user("nisse@pisse.se")
        self.login_user(user)
        self.assertEquals(func(self.url).status_code, 403)

    @staticmethod
    def _get_default_post_object():
        return {
            "name": "Test Company",
            "company_types": get_company_type("buyer").id,
            "content_languages": get_language("SV").id,
            "external_website_url": "",
        }
