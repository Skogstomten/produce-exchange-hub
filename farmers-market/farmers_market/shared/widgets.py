from django.forms.widgets import ChoiceWidget


class SearchableSelectWidget(ChoiceWidget):
    template_name = "/shared/widget_templates/searchable_select_input.html"
