from datetime import datetime
from typing import List, Dict

from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel

from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


class NewsFeedPostModel(BaseModel):
    language_iso: str
    title: str
    body: str

    @classmethod
    def create(
            cls,
            language: str,
            data: Dict[str, str]
    ):
        return cls(
            language_iso=language,
            title=data.get('title'),
            body=data.get('body')
        )


class NewsFeedFullOutModel(BaseModel):
    id: str
    posted_by_email: str
    posted_by_name: str
    posted_date: datetime
    post: List[NewsFeedPostModel]

    @classmethod
    def create(
            cls,
            post_id: str,
            data: Dict[str, DocumentReference | datetime | Dict[str, Dict[str, str]]],
            headers: AppHeaders
    ):
        user_ref = data.get('posted_by')
        user_snapshot = user_ref.get(('first_name', 'last_name',))
        user_data = user_snapshot.to_dict()
        posted_by_email = user_ref.id
        posted_by_name = f"{user_data.get('first_name')} {user_data.get('last_name')}"
        post_data = data.get('post')
        return cls(
            id=post_id,
            posted_by_email=posted_by_email,
            posted_by_name=posted_by_name,
            posted_date=format_datetime(data.get('posted_date'), headers.timezone),
            post=[
                NewsFeedPostModel.create(language, post_data.get(language))
                for language in post_data
            ]
        )
