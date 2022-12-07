from django.test import TestCase, Client
from django.urls import reverse

from . import models


def _create_user() -> tuple[models.User, str, str]:
    username = "nisse"
    password = "test123"
    return models.User.objects.create_user(username, "nisse@persson.se", password), username, password


def _create_company_with_admin() -> tuple[models.Company, models.User, str, str]:
    company = _create_company()
    role = _create_company_admin_role()
    user, username, password = _create_user()
    models.CompanyUser.objects.create(company=company, role=role, user=user)
    return company, user, username, password


def _create_company_admin_role() -> models.CompanyRole:
    return models.CompanyRole.objects.create(role_name="company_admin")


def _get_or_create(model, selectors, create_fields=None):
    if not create_fields:
        create_fields = selectors
    try:
        result = model.objects.get(**selectors)
    except model.DoesNotExist:
        result = model.objects.create(**create_fields)
    return result


def _get_company_type(name: str) -> models.CompanyType:
    return _get_or_create(models.CompanyType, {"type_name": name})


def _get_language(iso_639_1):
    return _get_or_create(models.Language, {"iso_639_1": iso_639_1}, {"iso_639_1": iso_639_1, "name": "Whatever"})


def _create_company() -> models.Company:
    status = models.CompanyStatus.objects.create(status_name="active", description="active")
    return models.Company.objects.create(name="Nisses firma", status=status)


class EditCompanyViewTest(TestCase):
    def test_post_returns_200(self):
        company, _, username, password = _create_company_with_admin()
        self.client.login(username=username, password=password)
        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_returns_202(self):
        company, _, username, password = _create_company_with_admin()

        if not self.client.login(username=username, password=password):
            self.fail("Login failed")

        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.post(
            url,
            {
                "company_name": "Test Company",
                "company_types": _get_company_type("buyer").id,
                "content_languages": _get_language("sv").id,
                "external_website_url": "",
            },
            follow=True,
        )

        self.assertEquals(response.status_code, 202)


class CompanyModelTest(TestCase):
    def test_is_company_admin_user_is_admin(self):
        company, user, _, _ = _create_company_with_admin()

        company = models.Company.objects.get(pk=company.id)
        self.assertTrue(company.is_company_admin(user))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(_create_company().is_company_admin(_create_user()[0]))
