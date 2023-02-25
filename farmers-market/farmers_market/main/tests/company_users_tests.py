from django.urls import reverse
from django.contrib.auth.models import User

from .test_helpers import TestCase, create_company_with_logged_in_admin, PASSWORD, get_company_admin_role
from ..models import CompanyUser


class CompanyUsersViewTest(TestCase):
    def test_can_delete_user(self):
        company, _ = create_company_with_logged_in_admin(self.client)
        other_user = User.objects.create_user("egon@persson.se", "egon@persson.se", PASSWORD)
        CompanyUser.objects.create(company=company, user=other_user, role=get_company_admin_role())

        response = self.client.post(reverse("main:delete_company_user", args=(company.id, other_user.id)), follow=True)

        try:
            CompanyUser.objects.get(company=company, user=other_user)
        except CompanyUser.DoesNotExist:
            pass
        else:
            self.fail("CompanyUser not removed")

        self.assertRedirects(
            response,
            expected_url=reverse("main:company_users", args=(company.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )
