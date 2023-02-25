from django.urls import reverse

from .test_helpers import TestCase, create_company_with_logged_in_admin, get_contact_type
from ..models import Contact


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
