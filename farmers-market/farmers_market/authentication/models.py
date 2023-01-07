from django.db.models import Model, OneToOneField, ForeignKey, CharField, ImageField, CASCADE, PROTECT
from django.contrib.auth.models import User


class ExtendedUser(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="ext")
    profile_picture = ImageField(upload_to="user_profile_picture", null=True, blank=True, default=None)
    county = CharField(max_length=100, null=True, blank=True, default=None)

    @classmethod
    def create_ext_user(cls, user: User, county: str = None) -> "ExtendedUser":
        return cls.objects.create(user=user, county=county)


def create_new_user(email: str, first_name: str, last_name: str, password: str, county: str | None) -> User:
    user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
    ExtendedUser.create_ext_user(user, county)
    return user
