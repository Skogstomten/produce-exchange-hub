from app.utils.lang_utils import select_localized_text
from app.models.v1.shared import Language


def test_select_localized_text_returns_none_if_none_is_found():
    data: dict[str, str] = {}
    result = select_localized_text(data, Language.sv, ['sv'])
    assert result is None


def test_select_localized_text_gets_text_if_found():
    data: dict[str, str] = {'sv': 'This is wrong', 'en': 'This is right'}
    result = select_localized_text(data, Language.en, ['nb'])
    assert result == 'This is right'


def test_select_localized_text_gets_company_value_if_not_found():
    data: dict[str, str] = {'en': 'I want this'}
    result = select_localized_text(data, Language.sv, ['nb', 'sv', 'en'])
    assert result == 'I want this'
