from .test_helpers import TestCase, create_user, create_company
from ..models import Company, CompanyUser, CompanyType, CompanyRole


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company1 = create_company(name="test1", status="active")
        self.company2 = create_company(name="test2", status="active")
        self.user1 = create_user("nisse@persson.se")
        self.user2 = create_user("egon@ljung.se")
        self.user_order_admin = create_user("order_admin@mail.com")
        CompanyUser.create_company_admin(self.company1, self.user2)
        CompanyUser.create_company_admin(self.company2, self.user1)
        CompanyUser.create_order_admin(self.company1, self.user_order_admin)

    def test_has_company_role_order_admin(self):
        self.assertTrue(self.company1.has_company_role(self.user_order_admin, CompanyRole.RoleName.order_admin))

    def test_is_company_admin_user_is_admin(self):
        self.assertTrue(self.company1.is_company_admin(self.user2))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(self.company1.is_company_admin(self.user1))

    def test_creator_becomes_admin(self):
        user = create_user("jyrgen@nb.se")
        company = Company.create("Norrlands Bastuklubb", user)
        self.assertTrue(company.is_company_admin(user))

    def test_is_producer_on_producer(self):
        company = create_company(company_types=["producer"])
        self.assertTrue(company.is_producer())

    def test_is_producer_on_non_producer(self):
        company = create_company(company_types=["buyer"])
        self.assertFalse(company.is_producer())

    def test_is_producer_is_case_insensitive(self):
        CompanyType.objects.create(type_name="Producer")
        company = create_company(company_types=["Producer"])
        self.assertTrue(company.is_producer())

    def test_get_newest_returns_active_company(self):
        self.assertEqual(len(Company.get_newest("EN")), 2)

    def test_deactivated_company_is_not_returned_from_get_newest(self):
        company = create_company(name="This is deactivated", status="deactivated")
        companies = Company.get_newest("EN")
        company_names = [c.name for c in companies]
        self.assertNotIn(company.name, company_names)
