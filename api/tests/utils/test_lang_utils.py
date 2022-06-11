from unittest import TestCase

from app.utils.lang_utils import select_localized_text
from app.models.v1.shared import Language


class LangUtilsTest(TestCase):
    def test_select_localized_text_returns_none_if_none_is_found(self):
        data: dict[str, str] = {}
        result = select_localized_text(data, Language.sv, ['sv'])
        self.assertIsNone(result)

    def test_select_localized_text_gets_text_if_found(self):
        data: dict[str, str] = {'sv': 'This is wrong', 'en': 'This is right'}
        result = select_localized_text(data, Language.en, ['nb'])
        self.assertEqual(result, 'This is right')

    def test_select_localized_text_gets_company_value_if_not_found(self):
        data: dict[str, str] = {'en': 'I want this'}
        result = select_localized_text(data, Language.sv, ['nb', 'sv', 'en'])
        self.assertEqual(result, 'I want this')
