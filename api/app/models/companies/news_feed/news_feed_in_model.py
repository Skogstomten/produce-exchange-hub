from datetime import datetime
from typing import Dict

import pytz
from pydantic import BaseModel, Field

from ....dependencies.user import User
from ....datastores.base_datastore import BaseDatastore


class NewsFeedPostPostPutModel(BaseModel):
    title: str = Field(..., max_length=200)
    body: str = Field(...)


class NewsFeedInModel(BaseModel):
    post: Dict[str, NewsFeedPostPostPutModel] = Field(...)

    def to_database_dict(self, user: User, datastore: BaseDatastore):
        result = {
            'posted_by': datastore.get_user_ref(user.user_id),
            'posted_date': datetime.now(pytz.utc),
            'post': {},
        }
        for language in self.post:
            result['post'][language] = {
                'title': self.post.get(language).title,
                'body': self.post.get(language).body,
            }
        return result
