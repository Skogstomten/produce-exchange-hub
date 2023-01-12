from django.db.models import Model, OneToOneField, ForeignKey, CharField, ImageField, CASCADE, PROTECT
from django.contrib.auth.models import User

from shared.models import Country


class ExtendedUser(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="ext")
    profile_picture = ImageField(upload_to="user_profile_picture", null=True, blank=True, default=None)
    county = CharField(max_length=100, null=True, blank=True, default=None)
    country = ForeignKey(Country, on_delete=PROTECT, null=True, blank=True, default=None)

    @classmethod
    def create_ext_user(cls, user: User, county: str = None, country: Country = None) -> "ExtendedUser":
        return cls.objects.create(user=user, county=county, country=country)

    @classmethod
    def get_existing_or_new(cls, user: User) -> "ExtendedUser":
        try:
            ext_user = ExtendedUser.objects.get(user=user)
        except ExtendedUser.DoesNotExist:
            ext_user = ExtendedUser(user=user)
        return ext_user
