from django.http import HttpResponseForbidden, HttpRequest
from django.contrib.auth.mixins import AccessMixin

from .models import Company
from .utils import get_language


class CompanyAdminRequiredMixin(AccessMixin):
    """Mixin that requires logged in user being admin for specific company."""

    pk_name = "company_id"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        pk = kwargs.get(self.pk_name)
        company = Company.get(pk, get_language(request))
        if not company.is_company_admin(request.user):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
