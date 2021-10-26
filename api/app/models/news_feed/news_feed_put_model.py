from typing import List

from pydantic import BaseModel, Field


class NewsFeedPostPutModel(BaseModel):
    language_iso: str = Field(..., min_length=2, max_length=2)
    title: str = Field(..., max_length=200)
    body: str = Field(...)


class NewsFeedPutModel(BaseModel):
    posted_by_email: str = Field(...)
    post: List[NewsFeedPostPutModel] = Field(..., min_items=1)
