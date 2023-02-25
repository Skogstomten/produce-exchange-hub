from django.urls import reverse

from .test_helpers import TestCase, create_company, create_authenticated_user


class CompanyProfilePictureViewTest(TestCase):
    def test_non_company_admin_can_not_post_to_view(self):
        company = create_company()
        create_authenticated_user(self.client)

        url = reverse("main:company_profile_picture", args=(company.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)
