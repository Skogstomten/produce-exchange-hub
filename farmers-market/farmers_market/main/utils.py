from django.http import HttpRequest
from django.conf import settings


def get_language(request: HttpRequest) -> str:
    return request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
