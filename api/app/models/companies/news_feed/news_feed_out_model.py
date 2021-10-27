from datetime import datetime
from typing import List, Dict

from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore
from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


class NewsFeedPostModel(BaseModel):
    title: str
    body: str

    @classmethod
    def create(cls, data: Dict[str, str]):
        return cls(
            title=data.get('title'),
            body=data.get('body')
        )


class NewsFeedOutModel(BaseModel):
    id: str = Field(...)
    posted_by: str = Field(...)
    posted_by_name: str = Field(...)
    posted_date: datetime = Field(...)
    post: Dict[str, NewsFeedPostModel] = Field(...)
    post_localized: NewsFeedPostModel = Field(None)

    @classmethod
    def create(
            cls,
            post_id: str,
            data: Dict[str, DocumentReference | datetime | Dict[str, Dict[str, str]]],
            headers: AppHeaders,
            datastore: BaseDatastore
    ):
        user_ref = data.get('posted_by')
        user_snapshot = user_ref.get(('first_name', 'last_name',))
        user_data = user_snapshot.to_dict()
        posted_by_email = user_ref.id
        posted_by_name = f"{user_data.get('first_name')} {user_data.get('last_name')}"
        post_data = data.get('post')
        post: Dict[str, NewsFeedPostModel] = {}
        for language in post_data:
            post[language] = NewsFeedPostModel.create(post_data.get(language))

        return cls(
            id=post_id,
            posted_by=posted_by_email,
            posted_by_name=posted_by_name,
            posted_date=format_datetime(data.get('posted_date'), headers.timezone),
            post=post,
            post_localized=datastore.localize(post_data, headers.language, company_languages)
        )
