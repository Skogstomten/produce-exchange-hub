from django.urls import reverse

from .test_helpers import TestCase, create_authenticated_user
from ..models import Company


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
