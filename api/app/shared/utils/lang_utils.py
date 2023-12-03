"""
Utility functions related to language handling.
"""
from app.database.enums import Language


def select_localized_text(data: dict[str | Language, str], lang: Language, company_languages: list[Language]) -> str:
    """
    Selects localized text from dict for given language or first available
    of company's languages if the requested
    language is not available.

    >>> select_localized_text({"SV": "Some text"}, Language.EN, [])
    ''

    >>> d: dict[str, str] = {"SV": "This is wrong", "EN": "This is right"}
    >>> select_localized_text(d, Language.EN, [Language.EN])
    'This is right'

    >>> d: dict[str, str] = {"EN": "I want this"}
    >>> select_localized_text(d, Language.SV, [Language.SV, Language.EN])
    'I want this'

    >>> d: dict[Language, str] = {Language.EN: "This is it"}
    >>> select_localized_text(d, Language.EN, [])
    'This is it'

    :param data: dict of str or Language, str with languagecode as key and translated text
    as value.
    :param lang:
    :param company_languages:
    :return:
    """
    value = data.get(lang.value, None) or data.get(lang, None)
    if value is None:
        for company_lang in company_languages:
            value = data.get(company_lang.value, None)
            if value is not None:
                break
    return value or ""
