from fastapi import APIRouter
from starlette.requests import Request

from app.models.v1.shared import Language


def assemble_url(*args, **kwargs) -> str:
    """
    *************
    Examples:

    >>> assemble_url("http://localhost:8000/", "/v1/{lang}/companies", "619676eb51b9ece53cbccb9b")
    'http://localhost:8000/v1/{lang}/companies/619676eb51b9ece53cbccb9b'

    >>> assemble_url("http://localhost:8000/", "/v1/{lang}/companies", "619676eb51b9ece53cbccb9b", lang="sv")
    'http://localhost:8000/v1/sv/companies/619676eb51b9ece53cbccb9b'

    :param args:
    :return:
    """
    url = "/".join(str(s).strip("/") for s in args)
    for key, value in kwargs.items():
        url = url.replace("{" + key + "}", str(value))
    return url


def assemble_profile_picture_url(request: Request, router: APIRouter, file_path: str, lang: Language) -> str:
    return assemble_url(
        request.base_url,
        router.prefix,
        file_path,
        lang=lang,
    )
