from django.http import HttpRequest, HttpResponseRedirect
from django.utils import translation
from django.conf import settings


def set_lang(request: HttpRequest):
    redirect_to = request.GET.get("next", None)
    if not redirect_to:
        redirect_to = request.META.get("HTTP_REFERER", None)
    if not redirect_to:
        redirect_to = "/"
    response = HttpResponseRedirect(redirect_to)
    lang = request.GET.get("lang", None)
    if lang:
        translation.activate(lang)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
