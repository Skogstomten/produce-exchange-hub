from django.urls import reverse

from .test_helpers import TestCase, create_company_with_logged_in_admin, get_contact_type
from ..models import Contact


class DeleteContactViewTest(TestCase):
    def test_can_delete_contact(self):
        company, _ = create_company_with_logged_in_admin(self.client)
        contact = Contact.create_contact(company, get_contact_type("email"), "nisse@perssons.se")
        response = self.client.post(reverse("main:delete_contact", args=(company.id, contact.id)))
        self.assertEqual(302, response.status_code)
