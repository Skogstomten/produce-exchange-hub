from django.forms import ModelForm, FileField, FloatField, FileInput, HiddenInput
from django.utils.translation import gettext_lazy as _

from PIL import Image


class UploadCroppedPictureModelForm(ModelForm):
    x = FloatField(widget=HiddenInput)
    y = FloatField(widget=HiddenInput)
    width = FloatField(widget=HiddenInput)
    height = FloatField(widget=HiddenInput)
    profile_picture = FileField(required=True, label=_("Upload profile picture"), widget=FileInput(attrs={"class": "crop-image"}))

    size: tuple[int, int] = (300, 300)

    class Meta:
        fields = ["profile_picture", "x", "y", "width", "height"]

    def save(self):
        instance = super().save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        Image.open(instance.profile_picture).crop((x, y, x + width, y + height)).resize(self.size, Image.ANTIALIAS).save(
            instance.profile_picture.path
        )

        return instance
