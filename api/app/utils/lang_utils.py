from ..models.v1.shared import Language


def select_localized_text(data: dict[str, str], lang: Language, company_languages: list[str]) -> str:
    value = data.get(lang.value)
    if value is None:
        for company_lang in company_languages:
            value = data.get(company_lang)
            if value is not None:
                break
    return value
