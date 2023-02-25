from django.urls import reverse
from django.contrib.auth.models import User

from main.tests.test_helpers import TestCase, create_company_with_admin, PASSWORD
from main.models import Currency, OrderType, Order, CompanyUser, Company


class EditOrderTest(TestCase):
    def setUp(self):
        self.company, self.user = create_company_with_admin(("buyer", "producer"))
        self.order = Order.add(self.company, "Cucumber", 10, "st", Currency.SEK, OrderType.SELL)
        self.url = reverse(
            "main:update_orders",
            args=(self.company.id,),
        )

    def test_can_not_call_with_get(self):
        self.assertEqual(404, self.client.get(self.url).status_code)

    def test_admin_can_update_order(self):
        self.login_user(self.user)
        self.assertRedirects(
            self.client.post(self.url, self._get_post_object(), follow=True),
            reverse("main:edit_company", args=(self.company.id,)),
        )

    def test_order_admin_can_update_order(self):
        order_admin = User.objects.create_user("IAdminOrders@gmail.com", "IAdminOrders@gmail.com", PASSWORD)
        CompanyUser.create_order_admin(self.company, order_admin)
        self.login_user(order_admin)
        self.assertRedirects(
            self.client.post(self.url, self._get_post_object(), follow=True),
            reverse("main:edit_company", args=(self.company.id,)),
        )

    def test_non_company_user_can_not_update_order(self):
        self.login_user(User.objects.create_user("otheruser", "otheruser@mail.com", PASSWORD))
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()).status_code)

    def test_admin_of_other_company_can_not_update_order(self):
        other_admin = User.objects.create_user("otheradmin", "otheradmin@mail.com", PASSWORD)
        Company.create("ShittyCompany", other_admin)
        self.login_user(other_admin)
        self.assertEqual(403, self.client.post(self.url, self._get_post_object()).status_code)

    def test_order_data_is_updated_correctly(self):
        self.login_user(self.user)
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
