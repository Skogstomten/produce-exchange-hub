from django.urls import reverse

from main.tests.test_helpers import TestCase, create_company, get_status


class IndexTest(TestCase):
    url = reverse("main:index")

    def setUp(self):
        self.active_company = create_company(name="Nisses firma", status=get_status("active"))

    def test_active_company_displayed_on_start_page(self):
        self.assertContains(self.client.get(self.url), "Nisses firma")
