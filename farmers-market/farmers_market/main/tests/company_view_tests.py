from django.urls import reverse

from main.tests.test_helpers import TestCase, create_company
from main.models import CompanyType, Order, Currency, OrderType


class CompanyViewTest(TestCase):
    def setUp(self):
        self.company = create_company(company_types=(CompanyType.TypeName.PRODUCER,))
        self.url = reverse("main:company", args=(self.company.id,))
        self.order = Order.add(self.company, "Cucumber", 10, "st", Currency.SEK, OrderType.SELL)

    def test_order_is_displayed_on_company_view(self):
        self.assertContains(self.client.get(self.url), self.order.product)
