from django.contrib.auth.models import User

from .test_helpers import TestCase, get_status, get_company_admin_role, create_user, create_company, PASSWORD
from ..models import Company, CompanyUser, CompanyType, CompanyRole


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company1 = Company.objects.create(name="test1", status=get_status("active"))
        self.company2 = Company.objects.create(name="test2", status=get_status("active"))
        self.user1 = User.objects.create_user("nissepisse", "nisse@persson.se", PASSWORD)
        self.user2 = User.objects.create_user("egon", "egon@ljung.se", PASSWORD)
        self.user_order_admin = User.objects.create_user("order_admin", "order_admin@mail.com", PASSWORD)
        CompanyUser.objects.create(company=self.company1, user=self.user2, role=get_company_admin_role())
        CompanyUser.objects.create(company=self.company2, user=self.user1, role=get_company_admin_role())
        CompanyUser.create_order_admin(self.company1, self.user_order_admin)

    def test_has_company_role_order_admin(self):
        self.assertTrue(self.company1.has_company_role(self.user_order_admin, CompanyRole.RoleName.order_admin))

    def test_is_company_admin_user_is_admin(self):
        self.assertTrue(self.company1.is_company_admin(self.user2))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(self.company1.is_company_admin(self.user1))

    def test_creator_becomes_admin(self):
        user = create_user()
        company = Company.create("Norrlands Bastuklubb", user.id)
        self.assertTrue(company.is_company_admin(user))

    def test_is_producer_on_producer(self):
        company = create_company(["producer"])
        self.assertTrue(company.is_producer())

    def test_is_producer_on_non_producer(self):
        company = create_company(["buyer"])
        self.assertFalse(company.is_producer())

    def test_is_producer_is_case_insensitive(self):
        CompanyType.objects.create(type_name="Producer")
        company = create_company(["Producer"])
        self.assertTrue(company.is_producer())
