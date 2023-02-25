from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from django.http import HttpResponseForbidden

from ..decorators import company_role_required
from .test_helpers import TestCase, PASSWORD
from ..models import Company, CompanyUser


@company_role_required
def i_require_company_admin_role(req, company_id) -> bool:
    if req and company_id:
        pass
    return True


@company_role_required(company_roles=("order_admin",))
def i_require_company_admin_or_order_admin(request, *, company_id) -> bool:
    if request and company_id:
        pass
    return True


class CompanyRoleRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", email="admin@mail.com", password=PASSWORD)
        self.order_admin = User.objects.create_user(
            username="order_admin", email="order_admin@mail.com", password=PASSWORD
        )
        self.company = Company.create("IIsCompany", self.admin_user)
        CompanyUser.create_order_admin(self.company, self.order_admin)
        self.r_factory = RequestFactory()
        self.request = self.r_factory.get(reverse("main:edit_company", args=(self.company.id,)))

    def test_company_admin_can_get_passed_company_role_required(self):
        self.login_user(self.admin_user)
        self.assertTrue(i_require_company_admin_role(self.request, company_id=self.company.id))

    def test_company_admin_can_get_passed_company_admin_or_order_admin_required(self):
        self.login_user(self.admin_user)
        self.assertTrue(i_require_company_admin_or_order_admin(self.request, company_id=self.company.id))

    def test_order_admin_can_get_passed_company_admin_or_order_admin_required(self):
        self.login_user(self.order_admin)
        self.assertTrue(i_require_company_admin_or_order_admin(self.request, company_id=self.company.id))

    def test_order_admin_can_not_get_passed_company_admin_required(self):
        self.login_user(self.order_admin)
        self.assertIsInstance(
            i_require_company_admin_role(self.request, company_id=self.company.id), HttpResponseForbidden
        )

    def login_user(self, user: User):
        super().login_user(user)
        self.request.user = user
