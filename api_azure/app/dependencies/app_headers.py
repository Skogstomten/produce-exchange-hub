from fastapi import Header


class AppHeaders(object):
    language: str
    timezone: str

    def __init__(self, language: str, timezone: str):
        self.language = language
        self.timezone = timezone


def get_headers(
        language: str = Header('SV', min_length=2, max_length=2),
        timezone: str = Header('Europe/Stockholm'),
) -> AppHeaders:
    return AppHeaders(language, timezone)
