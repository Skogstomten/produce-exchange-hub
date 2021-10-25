from datetime import datetime
from typing import Dict, List

from google.cloud.firestore_v1 import DocumentReference
from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore
from app.dependencies.app_headers import AppHeaders
from app.utilities.datetime_utilities import format_datetime


class NewsFeedOutModel(BaseModel):
    id: str
    title: str
    body: str
    posted_date: datetime
    posted_by_email: str
    posted_by_name: str

    @staticmethod
    def create(
            post_id: str,
            data: Dict[str, datetime | DocumentReference | Dict[str, str]],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ) -> Dict:
        post = datastore.localize(data.get('post'), headers.language, company_languages, {})
        user_ref: DocumentReference = data.get('posted_by')
        user_snapshot = user_ref.get()
        user_data = user_snapshot.to_dict()
        return {
            'id': post_id,
            'title': post.get('title'),
            'body': post.get('body'),
            'posted_date': format_datetime(data.get('posted_date'), headers.timezone),
            'posted_by_email': user_ref.id,
            'posted_by_name': f"{user_data.get('first_name')} {user_data.get('last_name')}",
        }
