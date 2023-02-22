"""farmers_market URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import set_lang

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("auth/", include("authentication.urls")),
    path("set_lang/", set_lang, name="set_lang"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
