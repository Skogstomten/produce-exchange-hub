from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .forms import LoginForm
from .models import ExtendedUser


class LoginViewTest(TestCase):
    def setUp(self):
        _, username, password = _create_user()
        self.post_data = {"email": username, "password": password}

    def test_post_returns_302(self):
        response = self.client.post(
            reverse("authentication:login"), self.post_data
        )
        self.assertEqual(response.status_code, 302)


class LoginFormTest(TestCase):
    def setUp(self):
        _, username, password = _create_user()
        req_factory = RequestFactory()
        self.post_data = {"email": username, "password": password}
        self.req = req_factory.post(reverse("authentication:login"), self.post_data)

    def test_is_valid_returns_true_if_user_authenticates(self):
        target = LoginForm(self.post_data)
        self.assertTrue(target.is_valid(self.req))
    
    def test_authenticate_works(self):
        target = LoginForm(self.post_data)
        target.is_valid(self.req)
        self.assertIsNotNone(authenticate(self.req, **target.get_credentials()))


def _create_user() -> tuple[User, str, str]:
    username = "nisse@persson.se"
    password = "test123"
    user = User.objects.create_user(username, username, password)
    ExtendedUser.create_ext_user(user)
    return user, username, password