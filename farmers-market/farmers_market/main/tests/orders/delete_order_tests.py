from django.urls import reverse

from main.tests.test_helpers import TestCase, create_company_with_admin, create_user
from main.models import Order, Currency, OrderType, CompanyUser


class DeleteOrderTest(TestCase):
    def setUp(self):
        self.company, self.admin_user = create_company_with_admin(("producer", "buyer"))
        self.order_admin_user = create_user("order_admin@mail.com")
        CompanyUser.create_order_admin(self.company, self.order_admin_user)
        self.order = Order.add(self.company, "Cucumber", 10, "st", Currency.SEK, OrderType.SELL)
        self.delete_order_url = reverse("main:delete_order", args=(self.company.id, self.order.id,))
        self.redirect_to_url = reverse("main:edit_company", args=(self.company.id,))

    def test_company_admin_can_delete_order(self):
        self.login_user(self.admin_user)
        self.assertRedirects(self.client.post(self.delete_order_url, follow=True), self.redirect_to_url)

    def test_order_admin_can_delete_order(self):
        self.login_user(self.order_admin_user)
        self.assertRedirects(self.client.post(self.delete_order_url, follow=True), self.redirect_to_url)

    def test_non_company_user_can_not_delete_order(self):
        self.login_user(create_user("other_user@mail.com"))
        self.assertEqual(self.client.post(self.delete_order_url).status_code, 403)

    def test_order_is_deleted(self):
        self.login_user(self.admin_user)
        self.client.post(self.delete_order_url)
        self.assertEqual(self.company.orders.all().count(), 0)
