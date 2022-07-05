"""
Essential dependencies for endpoints.
"""
from datetime import tzinfo

from fastapi import Request, Path, Depends
from pytz import timezone

from app.dependencies.timezone_header import get_timezone_header
from app.models.v1.shared import Language


class Essentials:
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


def get_essentials(
    request: Request,
    lang: Language = Path(...),
    tz: str = Depends(get_timezone_header),
) -> Essentials:
    """
    DI function for essential dependencies
    :param request: HTTP Request.
    :param lang: Language as Enum.
    :param tz: Timezone from timezone header.
    :return: Essentials dependency.
    """
    return Essentials(
        request,
        lang,
        tz,
    )
