from django.contrib.auth.models import User
from django.urls import reverse

from .test_helpers import create_company_with_admin, PASSWORD, TestCase
from ..models import CompanyUser, Company, CompanyStatus


class DeactivateCompanyTest(TestCase):
    def setUp(self):
        self.company, self.admin = create_company_with_admin()
        self.order_admin = User.objects.create_user("order_admin", "order_admin@mail.com", PASSWORD)
        CompanyUser.create_order_admin(self.company, self.order_admin)
        self.other_user = User.objects.create_user("other_user", "other_user@mail.com", PASSWORD)
        self.deactivate_company_url = reverse("main:deactivate_company", args=(self.company.id,))
        self.redirect_to_url = reverse("main:edit_company", args=(self.company.id,))
        self.edit_company_url = self.redirect_to_url

    def test_company_admin_can_deactivate_company(self):
        self.login_user(self.admin)
        self.assertRedirects(self.client.post(self.deactivate_company_url, follow=True), self.redirect_to_url)

    def test_order_admin_can_not_deactivate_company(self):
        self.login_user(self.order_admin)
        self.assertEqual(self.client.post(self.deactivate_company_url, follow=True).status_code, 403)

    def test_non_company_user_can_not_deactivate_company(self):
        self.login_user(self.order_admin)
        self.assertEqual(self.client.post(self.deactivate_company_url).status_code, 403)

    def test_company_admin_of_other_company_can_not_deactivate_company(self):
        Company.create("Shit company", self.other_user)
        self.login_user(self.other_user)
        self.assertEqual(self.client.post(self.deactivate_company_url).status_code, 403)

    def test_deactivate_button_is_rendered_on_page_for_company_admin(self):
        self.login_user(self.admin)
        self.assertContains(self.client.get(self.edit_company_url), '<form id="deactivateCompanyForm"')

    def test_deactivate_button_is_not_rendered_on_page_for_order_admin(self):
        self.login_user(self.order_admin)
        self.assertNotContains(self.client.get(self.edit_company_url), '<form id="deactivateCompanyForm"')

    def test_company_status_is_updated_correctly_on_deactivation(self):
        self.login_user(self.admin)
        self.client.post(self.deactivate_company_url)
        self.assertEqual(Company.get(self.company.id).status.status_name, CompanyStatus.StatusName.deactivated.value)

    def test_deactivate_button_not_displayed_after_company_has_been_deactivated(self):
        self.login_user(self.admin)
        self.assertNotContains(
            self.client.post(self.deactivate_company_url, follow=True), '<form id="deactivateCompanyForm"'
        )

    def test_deactivated_company_does_not_show_up_on_index_page(self):
        self.login_user(self.admin)
        self.assertRedirects(self.client.post(self.deactivate_company_url, follow=True), self.redirect_to_url)
        self.assertNotContains(self.client.get(reverse("main:index")), self.company.name)
