from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Company, Language, CompanyType, CompanyUser, CompanyRole, CompanyStatus, ContactType, Contact


class AddContactViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

    def test_can_add_contact(self):
        company, _ = _create_company_with_logged_in_admin(self.client)
        response = self.client.post(
            reverse("main:add_contact", args=(company.id,)),
            {
                "company": company.id,
                "contact_type": _get_contact_type("email").id,
                "value": "nisse@perssons.se",
                "description": "Boss",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        contact = Contact.objects.get(value="nisse@perssons.se")
        self.assertEqual(contact.company.name, company.name)
        self.assertEqual(contact.description, "Boss")


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
        self.assertRedirects(
            response,
            reverse("main:edit_company", args=(company.id,)),
            target_status_code=200,
            fetch_redirect_response=True,
        )


class CompanyProfilePictureViewTest(TestCase):
    def setUp(self):
        _setup_defaults()

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
        self.company1 = Company.objects.create(name="test1", status=_get_status("active"))
        self.company2 = Company.objects.create(name="test2", status=_get_status("active"))
        self.user1 = User.objects.create_user("nissepisse", "nisse@persson.se", "test123")
        self.user2 = User.objects.create_user("egon", "egon@ljung.se", "test123")
        CompanyUser.objects.create(company=self.company1, user=self.user2, role=_get_company_admin_role())
        CompanyUser.objects.create(company=self.company2, user=self.user1, role=_get_company_admin_role())

    def test_is_company_admin_user_is_admin(self):
        self.assertTrue(self.company1.is_company_admin(self.user2))

    def test_is_company_admin_user_is_not_admin(self):
        self.assertFalse(self.company1.is_company_admin(self.user1))

    def test_creator_becomes_admin(self):
        user, _, _ = _create_user()
        company = Company.create("Norrlands Bastuklubb", user.id)
        self.assertTrue(company.is_company_admin(user))


def _get_default_post_object():
    return {
        "name": "Test Company",
        "company_types": _get_company_type("buyer").id,
        "content_languages": _get_language("SV").id,
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


def _get_company_type(type_name: str) -> CompanyType:
    return CompanyType.objects.get(type_name=type_name)


def _get_language(iso_639_1):
    return Language.objects.get(iso_639_1=iso_639_1)


def _get_status(status_name):
    return CompanyStatus.objects.get(status_name=status_name)


def _create_company() -> Company:
    return Company.objects.create(name="Nisses firma", status=_get_status("active"))


def _get_contact_type(contact_type) -> ContactType:
    return ContactType.objects.get(contact_type=contact_type)


def _setup_defaults():
    CompanyRole.objects.create(role_name="company_admin")
    CompanyStatus.objects.create(status_name="created")
    CompanyStatus.objects.create(status_name="active")
    Language.objects.create(iso_639_1="SV")
    Language.objects.create(iso_639_1="EN")
    CompanyType.objects.create(type_name="producer")
    CompanyType.objects.create(type_name="buyer")
    ContactType.objects.create(contact_type="email")
    ContactType.objects.create(contact_type="phone")
