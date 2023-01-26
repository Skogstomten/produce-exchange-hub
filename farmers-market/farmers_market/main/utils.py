from django.http import HttpRequest
from django.conf import settings


def get_language(request: HttpRequest) -> str:
    return request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)


def get_localized_value_from_dataset(language: str, dataset, field_name: str) -> str | None:
    """Write good description."""
    localization = next(iter(l for l in dataset if l.language.iso_639_1.upper() == language), None)
    if localization:
        return getattr(localization, field_name)
    return None


def get_localized_value_from_object(
    obj, language: str, related_field_name: str, related_field_field_name: str, get_content_languages: callable
) -> str:
    if len(language) > 2:
        language = language[:2].upper()
    dataset = getattr(obj, related_field_name).all()
    value = get_localized_value_from_dataset(language, dataset, related_field_field_name)
    if not value:
        for content_language in get_content_languages():
            value = get_localized_value_from_dataset(
                content_language.iso_639_1.upper(), dataset, related_field_field_name
            )
            if value:
                break
    return value or next(iter(getattr(d, related_field_field_name) for d in dataset), "")
