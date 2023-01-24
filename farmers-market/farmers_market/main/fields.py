from django.forms import Field, HiddenInput, EmailInput, ValidationError
from django.core.validators import EmailValidator
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class UserField(Field):
    widget = EmailInput
    label = _("User e-mail")
    validators = EmailValidator()

    def clean(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist as err:
            raise ValidationError(_("User not found"), "user_not_found") from err
        return user


class ForeignKeyRefField(Field):
    def __init__(
        self,
        fk_type,
        initial=None,
    ):
        if not issubclass(fk_type, Model):
            raise ValueError("fk_type has to be a subclass of django.db.models.Model")

        super().__init__(
            required=True,
            widget=HiddenInput,
            label=None,
            initial=initial,
            help_text=None,
            error_messages=None,
            show_hidden_initial=False,
            validators=(),
            localize=False,
            disabled=False,
            label_suffix=None,
        )

        self.fk_type = fk_type

    def clean(self, value):
        value = int(value)
        fk_obj = self.fk_type.objects.get(pk=value)
        if not fk_obj:
            raise ValidationError(f"Value is not a valid pk for {self.fk_type.__qualname__}", code="obj_not_found")
        return fk_obj
