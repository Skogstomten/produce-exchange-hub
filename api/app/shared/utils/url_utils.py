from fastapi import APIRouter, Request

from app.shared.models.v1.shared import Language


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


def assemble_profile_picture_url(
    request: Request, router: APIRouter, file_path: str | None, lang: Language
) -> str | None:
    """
    Will assemble absolute url for profile picture.

    If file_path is None, None will be returned.

    :param request: Http request object.
    :param router: fastapi router.
    :param file_path: Relative path to file.
    :param lang:
    :return: Profile picture url as str or None if there's no file_path.
    """
    if not file_path:
        return None

    return assemble_url(
        request.base_url,
        router.prefix,
        file_path,
        lang=lang,
    )
