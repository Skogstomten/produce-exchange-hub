import pytz
from typing import Dict
from datetime import datetime

from pydantic import BaseModel, Field


class UserInModel(BaseModel):
    id: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    preferred_language_iso: str = Field(...)
    timezone: str = Field(...)

    def to_database_dict(
            self,
            user_id: str,
    ) -> Dict:
        now = datetime.now(pytz.utc)
        result = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_date': now,
            'last_logged_in': now,
            'preferred_language_iso': self.preferred_language_iso,
            'timezone': self.timezone,
            'profile_picture_url': None,
            'is_super_user': False,
        }
        return result
