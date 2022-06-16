"""
Utility functions related to language handling.
"""
from ..models.v1.shared import Language


def select_localized_text(
    data: dict[str, str], lang: Language, company_languages: list[str]
) -> str:
    """
    Selects localized text from dict for given language or first available
    of company's languages if the requested
    language is not available.

    >>> select_localized_text({"sv": "Some text"}, Language.en, [])
    None

    :param data: dict of str, str with languagecode as key and translated text as value.
    :param lang:
    :param company_languages:
    :return:
    """
    value = data.get(lang.value)
    if value is None:
        for company_lang in company_languages:
            value = data.get(company_lang)
            if value is not None:
                break
    return value
