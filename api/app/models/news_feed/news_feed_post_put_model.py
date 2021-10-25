from typing import List

from pydantic import BaseModel, Field


class NewsFeedPostInModel(BaseModel):
    language_iso: str = Field(..., min_length=2, max_length=2)
    title: str
    body: str


class NewsFeedPostPutModel(BaseModel):
    user_id: str = Field(...)
    post: List[NewsFeedPostInModel] = Field(..., min_items=1)
