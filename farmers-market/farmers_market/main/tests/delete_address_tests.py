from django.urls import reverse

from .test_helpers import TestCase, create_company_with_logged_in_admin
from ..models import Address


class DeleteAddressViewTest(TestCase):
    def test_can_delete_address(self):
        company, _ = create_company_with_logged_in_admin(self.client)
        address = Address.objects.create(company=company, address_type="Shit")
        response = self.client.post(reverse("main:delete_address", args=(company.id, address.id)))
        self.assertEqual(response.status_code, 302)
