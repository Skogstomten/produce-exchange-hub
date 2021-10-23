from datetime import datetime

from app.errors import UnexpectedError
from app.datetime_helpers import format_date


class Notification(object):
    id: str
    title: str
    body: str
    notification_date: datetime
    read: bool

    def __init__(self,
                 notification_id: str,
                 data: dict[str, dict[str, str | datetime | bool]],
                 user_language: str,
                 company_languages: list[str]):
        self.id = notification_id

        notification: dict[str, str | datetime | bool] | None = None
        if user_language in data:
            notification = data.get(user_language)
        else:
            for company_language in company_languages:
                if company_language in data:
                    notification = data.get(company_language)
                    break

        if notification is not None:
            self.title = notification.get('title')
            self.body = notification.get('body')
            self.notification_date = notification.get('notification_date')
            self.read = notification.get('read')
        else:
            raise UnexpectedError(f"No notification data found for notification id='{notification_id}'")

    def to_dict(self) -> dict[str, str | bool]:
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'read': self.read,
            'notification_date': format_date(self.notification_date, 'Europe/Stockholm')
        }
