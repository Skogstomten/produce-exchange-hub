from datetime import datetime

from app.datetime_helpers import format_date


class User(object):
    id: str
    first_name: str
    last_name: str
    created_date: datetime
    is_super_user: bool
    last_logged_in: datetime
    preferred_language: str
    preferred_language_iso: str
    profile_picture_url: str
    timezone: str

    def __init__(self, user_id: str, data: dict[str, str | datetime | bool]):
        self.id = user_id
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.created_date = data.get('created_date')
        self.is_super_user = data.get('is_super_user')
        self.last_logged_in = data.get('last_logged_in')
        self.preferred_language = data.get('preferred_language')
        self.preferred_language_iso = data.get('preferred_language_iso')
        self.profile_picture_url = data.get('profile_picture_url')
        self.timezone = data.get('timezone', 'Europe/Stockholm')

    def to_dict(self) -> dict[str, str | bool]:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_date': format_date(self.created_date, self.timezone),
            'last_logged_in': format_date(self.last_logged_in, self.timezone),
            'is_super_user': self.is_super_user,
            'preferred_language': self.preferred_language,
            'preferred_language_iso': self.preferred_language_iso,
            'profile_picture_url': self.profile_picture_url,
            'timezone': self.timezone,
        }
