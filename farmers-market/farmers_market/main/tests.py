from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Company, Language, CompanyType, CompanyUser, CompanyRole, CompanyStatus


class NewCompanyViewTest(TestCase):
    url = reverse("main:new_company")

    def setUp(self):
        _setup_defaults()

    def test_get_returns_200(self):
        _create_authenticated_user(self.client)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
    
    def test_valid_post_returns_302(self):
        user = _create_authenticated_user(self.client)
        response = self.client.post(self.url, {"name": "Nisse", "user_id": user.id})
        self.assertEqual(302, response.status_code)
    
    def test_post_redirect(self):
        user = _create_authenticated_user(self.client)
        response = self.client.post(self.url, {"name": "TestCompany", "user_id": user.id}, follow=True)
        company = Company.objects.get(name="TestCompany")
        self.assertRedirects(response, reverse("main:edit_company", args=(company.id,)), target_status_code=200, fetch_redirect_response=True)


class CompanyProfilePictureViewTest(TestCase):
    def test_non_company_admin_can_not_post_to_view(self):
        company = _create_company()
        _create_authenticated_user(self.client)

        url = reverse("main:company_profile_picture", args=(company.id,))
        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)


class EditCompanyViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_get_returns_200(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_get_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.get(url))

    def test_post_returns_202(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.post(
            url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def test_post_requires_company_admin(self):
        self._method_requires_company_admin(lambda url: self.client.post(url, _get_default_post_object()))

    def test_post_can_remove_language(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        swe = _get_language("SV")
        eng = _get_language("EN")
        company.content_languages.add(swe, eng)
        company.save()

        url = reverse("main:edit_company", args=(company.id,))
        response = self.client.post(
            url,
            _get_default_post_object(),
        )

        self.assertEquals(response.status_code, 202)

    def _method_requires_company_admin(self, func):
        company = _create_company()
        _create_authenticated_user(self.client)
        url = reverse("main:edit_company", args=(company.id,))
        response = func(url)
        self.assertEquals(response.status_code, 403)


class CompanyModelTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_is_company_admin_user_is_admin(self):
        company, user, _, _ = _create_company_with_admin()

        company = Company.objects.get(pk=company.id)
        self.assertTrue(company.is_company_admin(user))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(_create_company().is_company_admin(_create_user()[0]))
    
    def test_creator_becomes_admin(self):
        user, _, _ = _create_user()
        company = Company.create("Norrlands Bastuklubb", user.id)
        self.assertTrue(company.is_company_admin(user))


def _get_default_post_object():
    return {
        "name": "Test Company",
        "company_types": _get_company_type("buyer").id,
        "content_languages": _get_language("sv").id,
        "external_website_url": "",
    }


def _create_user() -> tuple[User, str, str]:
    username = "nisse"
    password = "test123"
    user = User.objects.create_user(username, "nisse@persson.se", password)
    user.save()
    return user, username, password


def _create_authenticated_user(client: Client) -> User:
    user, username, password = _create_user()
    client.login(username=username, password=password)
    return user


def _create_company_with_admin() -> tuple[Company, User, str, str]:
    company = _create_company()
    role = _get_company_admin_role()
    user, username, password = _create_user()
    CompanyUser.objects.create(company=company, role=role, user=user)
    return company, user, username, password


def _create_company_with_logged_in_admin(client: Client) -> tuple[Company, User]:
    company, user, username, password = _create_company_with_admin()
    client.login(username=username, password=password)
    return company, user


def _get_company_admin_role() -> CompanyRole:
    return CompanyRole.objects.get(role_name="company_admin")


def _get_or_create(model, selectors, create_fields=None):
    if not create_fields:
        create_fields = selectors
    try:
        result = model.objects.get(**selectors)
    except model.DoesNotExist:
        result = model.objects.create(**create_fields)
    return result


def _get_company_type(name: str) -> CompanyType:
    return _get_or_create(CompanyType, {"type_name": name})


def _get_language(iso_639_1):
    return _get_or_create(Language, {"iso_639_1": iso_639_1}, {"iso_639_1": iso_639_1, "name": "Whatever"})


def _create_company() -> Company:
    status = CompanyStatus.objects.create(status_name="active", description="active")
    return Company.objects.create(name="Nisses firma", status=status)

def _setup_defaults():
    CompanyRole.objects.create(role_name="company_admin")
