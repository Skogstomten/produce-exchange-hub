"""
Essential dependencies for endpoints.
"""
from datetime import tzinfo

from fastapi import Request, Path, Depends
from pytz import timezone

from app.database.enums import Language
from app.shared.dependencies.timezone_header import get_timezone_header


class RequestContext:
    """
    Data holder for dependencies.
    """

    def __init__(
        self,
        request: Request,
        lang: Language,
        tz: str | tzinfo,
    ):
        self.request = request
        self.language = lang
        if isinstance(tz, str):
            self.timezone = timezone(tz)
        else:  # Will be tzinfo
            self.timezone = tz

    def __str__(self):
        return f"Essentials(request={self.request}, lang={self.language}, tz={self.timezone})"

    def __repr__(self):
        return self.__str__()


def get_request_context(
    request: Request,
    lang: Language = Path(...),
    tz: str = Depends(get_timezone_header),
) -> RequestContext:
    """
    DI function for essential dependencies
    :param request: HTTP Request.
    :param lang: Language as Enum.
    :param tz: Timezone from timezone header.
    :return: Essentials dependency.
    """
    return RequestContext(
        request,
        lang,
        tz,
    )
