from django.http import HttpRequest, HttpResponseRedirect
from django.utils import translation
from django.conf import settings

def set_lang(request: HttpRequest):
    next = request.GET.get("next", None)
    if not next:
        next = request.META.get("HTTP_REFERER", None)
    if not next:
        next = "/"
    response = HttpResponseRedirect(next)
    lang = request.GET.get("lang", None)
    if lang:
        translation.activate(lang)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
