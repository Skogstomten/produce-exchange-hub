from modeltranslation.translator import translator, TranslationOptions

from .models import CompanyType, Language


class CompanyTypeTranslationOptions(TranslationOptions):
    fields = ("type_name",)


class LanguageTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(CompanyType, CompanyTypeTranslationOptions)
translator.register(Language, LanguageTranslationOptions)
