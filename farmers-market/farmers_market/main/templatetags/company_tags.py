from django.template import Library
from django.contrib.auth.models import User

register = Library()


@register.inclusion_tag("main/tag_templates/user_companies.html")
def user_companies(user: User):
    return {
        "companies": [company_user.company for company_user in user.companies.all()],
    }
