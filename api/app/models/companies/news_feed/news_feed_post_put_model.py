from datetime import datetime
from typing import List

import pytz
from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore


class NewsFeedPostPostPutModel(BaseModel):
    language_iso: str = Field(..., min_length=2, max_length=2)
    title: str = Field(..., max_length=200)
    body: str = Field(...)


class NewsFeedPostPutModel(BaseModel):
    posted_by_email: str = Field(...)
    post: List[NewsFeedPostPostPutModel] = Field(..., min_items=1)

    def to_database_dict(self, datastore: BaseDatastore):
        result = {
            'posted_by': datastore.get_user_ref(self.posted_by_email),
            'posted_date': datetime.now(pytz.utc),
            'post': {},
        }
        for localization in self.post:
            result['post'][localization.language_iso] = {
                'title': localization.title,
                'body': localization.body,
            }
        return result
