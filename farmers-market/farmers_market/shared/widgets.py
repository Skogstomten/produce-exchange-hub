from typing import Mapping, Callable

from django.forms.widgets import Select
from django.db.models import QuerySet, Model
from django.db.models.fields.related import RelatedField


class SearchableSelectWidget(Select):
    template_name = "shared/widget_templates/searchable_select_input.html"

    def __init__(
        self,
        dataset: QuerySet | RelatedField,
        get_display_value: Callable[[Model], str],
        attrs: Mapping[str, str] = None,
    ):
        super().__init__(attrs, [(entity.id, get_display_value(entity)) for entity in dataset])
