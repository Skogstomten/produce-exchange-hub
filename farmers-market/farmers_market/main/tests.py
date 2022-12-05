from django.test import TestCase

from . import models


def _create_user() -> models.User:
    return models.User.objects.create_user("nisse", "nisse@persson.se", "test123")


def _create_company() -> models.Company:
    status = models.CompanyStatus.objects.create(status_name="active", description="active")
    return models.Company.objects.create(name="Nisses firma", status=status)


class CompanyModelTest(TestCase):
    def test_is_company_admin_user_is_admin(self):
        user = _create_user()
        role = models.CompanyRole.objects.create(role_name="company_admin")
        company = _create_company()
        models.CompanyUser.objects.create(company=company, user=user, role=role)

        company = models.Company.objects.get(pk=company.id)
        self.assertTrue(company.is_company_admin(user))
    
    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(_create_company().is_company_admin(_create_user()))
