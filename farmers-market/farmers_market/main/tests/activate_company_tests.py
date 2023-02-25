from django.urls import reverse
from django.contrib.auth.models import User

from .test_helpers import TestCase, create_company_with_admin, create_user, PASSWORD


class ActivateCompanyViewTest(TestCase):
    def setUp(self):
        (
            self.company_with_admin,
            self.company_admin_user,
        ) = create_company_with_admin()
        self.url = reverse("main:activate_company", args=(self.company_with_admin.id,))

    def test_http_get_returns_404(self):
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_successfull_activation_returns_302(self):
        self.login_user(self.company_admin_user)
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_non_admin_user_returns_403(self):
        user = create_user("nonadmin@test.se")
        self.login_user(user)
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_superuser_can_activate(self):
        username = "superuser@test.se"
        user = User.objects.create_superuser(username, username, PASSWORD)
        self.login_user(user)
        self.assertEqual(self.client.post(self.url).status_code, 302)

    def test_success_redirects_back_to_edit_company_view(self):
        self.login_user(self.company_admin_user)
        self.assertRedirects(
            self.client.post(self.url, follow=True),
            reverse("main:edit_company", args=(self.company_with_admin.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )
