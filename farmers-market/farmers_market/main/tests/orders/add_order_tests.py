from django.urls import reverse

from main.models import OrderType, Order, Currency, CompanyUser
from main.tests.test_helpers import create_company_with_admin, TestCase, create_authenticated_user, get_company_role


class AddOrderContainer:
    def __init__(self, endpoint_name: str, order_type: OrderType):
        (
            self.company,
            self.company_admin,
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
        test_case.login_user(self.company_admin)
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
