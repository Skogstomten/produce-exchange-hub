from typing import List

from pydantic import BaseModel, Field

from app.models.companies.in_models.company_post_put_model import AddressPostPutModel


class AddressesPutModel(BaseModel):
    addresses: List[AddressPostPutModel] = Field(...)
