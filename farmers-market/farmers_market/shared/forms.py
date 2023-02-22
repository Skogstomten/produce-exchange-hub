from PIL import Image
from django.db.models import Model
from django.forms import ModelForm, FileField, FloatField, FileInput, HiddenInput
from django.utils.translation import gettext_lazy as _


class UploadCroppedPictureModelForm(ModelForm):
    x = FloatField(widget=HiddenInput)
    y = FloatField(widget=HiddenInput)
    width = FloatField(widget=HiddenInput)
    height = FloatField(widget=HiddenInput)
    profile_picture = FileField(
        required=True, label=_("Upload profile picture"), widget=FileInput(attrs={"class": "crop-image"})
    )

    size: tuple[int, int] = (300, 300)

    def __init__(self, post_url: str, instance: Model, data=None, files=None, *args, **kwargs):
        super().__init__(data, files, instance=instance, *args, **kwargs)
        self.post_url = post_url

    class Meta:
        fields = ["profile_picture", "x", "y", "width", "height"]

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        width = self.cleaned_data.get("width")
        height = self.cleaned_data.get("height")

        Image.open(instance.profile_picture).crop((x, y, x + width, y + height)).resize(
            self.size, Image.ANTIALIAS
        ).save(instance.profile_picture.path)

        return instance
