from django.db.models import Model, CharField
from django.utils.translation import gettext_lazy as _


class Country(Model):
    country_iso_3166_1 = CharField(max_length=2, unique=True)
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.country_iso_3166_1} - {_(self.name)}"

    class Meta:
        verbose_name_plural = "Countries"
