from django.http import HttpResponseForbidden, HttpRequest
from django.contrib.auth.mixins import AccessMixin

from .models import Company
from .utils import get_language


class CompanyRoleRequiredMixin(AccessMixin):
    """Mixin that requires logged-in user being in a specific role for specific company."""

    pk_name = "company_id"
    role_names: list[str] | None = None

    def dispatch(self, request: HttpRequest, *args: tuple, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if args:
            pk = args[0]
        elif kwargs:
            pk = kwargs.get(self.pk_name)
        else:
            raise KeyError(f"No keyword argument {self.pk_name} was found")

        company = Company.get(pk, get_language(request))
        if not company.has_company_role(request.user, self.role_names):
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)
