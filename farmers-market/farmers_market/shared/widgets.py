"""Custom widgets."""
from typing import Mapping, Callable, Any

from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ChoiceWidget
from django.db.models import QuerySet, Model
from django.db.models.fields.related import RelatedField


class SearchableSelectWidget(ChoiceWidget):
    """A select box-ish that provides search functionallity to filter multiple values."""

    template_name = "shared/widget_templates/searchable_select_input.html"

    def __init__(
        self,
        dataset: QuerySet | RelatedField,
        get_display_value: Callable[[Model], str],
        attrs: Mapping[str, str] = {},
    ):
        """
        args:
            dataset:
                The data to be displayed in the drop down.
                Can either be of type django.db.models.QuerySet or django.db.models.fields.related.RelatedField.
                If the field is passed the all() method will be called to get all the data in the field.
            get_display_value:
                Selector function to select the display value of the data entity.

        Optional args:
            attrs:
                Any additional html attributes.
        """
        dataset = dataset if isinstance(dataset, QuerySet) else dataset.all()
        super().__init__(attrs, [(entity.id, get_display_value(entity)) for entity in dataset])
