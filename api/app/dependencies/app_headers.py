from fastapi import Header


class AppHeaders(object):
    language: str
    timezone: str
    user_id: str

    def __init__(self, language: str, timezone: str, user_id: str):
        self.language = language
        self.timezone = timezone
        self.user_id = user_id


def get_headers(
        language: str = Header('SV', min_length=2, max_length=2),
        timezone: str = Header('Europe/Stockholm'),
        user_id: str = Header(...)
) -> AppHeaders:
    return AppHeaders(language, timezone, user_id)
