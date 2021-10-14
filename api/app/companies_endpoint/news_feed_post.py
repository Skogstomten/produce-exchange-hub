from datetime import datetime

from google.cloud.firestore_v1 import DocumentReference

from app.datetime_helpers import format_date
from app.errors import UnexpectedError


class NewsFeedPost(object):
    id: str
    title: str
    body: str
    posted_by: DocumentReference
    posted_date: datetime

    def __init__(self,
                 post_id: str,
                 data: dict[str, dict[str, str | datetime | DocumentReference]],
                 user_language: str,
                 company_languages: list[str]):
        self.id = post_id
        post: dict[str, str | datetime | DocumentReference] | None = None
        if user_language in data:
            post = data[user_language]
        else:
            for company_language in company_languages:
                if company_language in data:
                    post = data[company_language]
                    break

        if post is not None:
            self.title = post.get('title')
            self.body = post.get('body')
            self.posted_by = post.get('posted_by')
            self.posted_date = post.get('posted_date')
        else:
            raise UnexpectedError(f"No news feed post data was found for post id: '{post_id}'")

    def to_dict(self) -> dict[str, str]:
        author_snapshot = self.posted_by.get()
        author_id = author_snapshot.id
        author = author_snapshot.to_dict()
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'posted_by_email': author_id,
            'posted_by_name': f"{author.get('first_name')} {author.get('last_name')}",
            'posted_date': format_date(self.posted_date, 'Europe/Stockholm'),
        }
