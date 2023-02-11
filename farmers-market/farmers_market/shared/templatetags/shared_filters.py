from django.template.library import Library

register = Library()


@register.filter
def hide_none(value):
    """Replaces None values with an empty str."""
    if value is None:
        return ""
    return value
