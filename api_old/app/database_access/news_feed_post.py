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
    updated_by: DocumentReference | None = None
    updated_date: datetime | None = None

    def __init__(self,
                 post_id: str,
                 data: dict[str, datetime | DocumentReference | dict[str, dict[str, str]]],
                 user_language: str,
                 company_languages: list[str]):
        self.id = post_id
        self.posted_by = data.get('posted_by')
        self.posted_date = data.get('posted_date')
        self.updated_by = data.get('updated_by', None)
        self.updated_date = data.get('updated_date', None)

        posts: dict[str, dict[str, str]] = data.get('post')
        post: dict[str, str] | None = None
        if user_language in posts:
            post = posts.get(user_language)
        else:
            for company_language in company_languages:
                if company_language in posts:
                    post = posts[company_language]
                    break

        if post is not None:
            self.title = post.get('title')
            self.body = post.get('body')
        else:
            raise UnexpectedError(f"No news feed post data was found for post id: '{post_id}'")

    def to_dict(self) -> dict[str, str]:
        author_snapshot = self.posted_by.get()
        author_id = author_snapshot.id
        author = author_snapshot.to_dict()
        result = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'posted_by_email': author_id,
            'posted_by_name': f"{author.get('first_name')} {author.get('last_name')}",
            'posted_date': format_date(self.posted_date, 'Europe/Stockholm'),
        }
        if self.updated_by is not None:
            updated_by = self.updated_by.get()
            updater = updated_by.to_dict()
            result['updated_by_email'] = updated_by.id
            result['updated_by_name'] = f"{updater.get('first_name')} {updater.get('last_name')}"

        if self.updated_date is not None:
            result['updated_date'] = format_date(self.updated_date, 'Europe/Stockholm')

        return result
