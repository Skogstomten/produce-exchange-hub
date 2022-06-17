from fastapi import Request, Path, Depends

from app.dependencies.timezone_header import get_timezone_header
from app.models.v1.shared import Language


class Essentials:
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
    return Essentials(
        request,
        lang,
        timezone,
    )
