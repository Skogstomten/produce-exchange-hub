"""
Essential dependencies for endpoints.
"""
from fastapi import Request, Path, Depends

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
        timezone: str,
    ):
        self.request = request
        self.language = lang
        self.timezone = timezone


def get_essentials(
    request: Request,
    lang: Language = Path(...),
    timezone: str = Depends(get_timezone_header),
) -> Essentials:
    """
    DI function for essential dependencies
    :param request: HTTP Request.
    :param lang: Language as Enum.
    :param timezone: Timezone from timezone header.
    :return: Essentials dependency.
    """
    return Essentials(
        request,
        lang,
        timezone,
    )
