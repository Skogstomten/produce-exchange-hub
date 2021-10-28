from typing import Optional, Dict

from pydantic import BaseModel, Field


class DeliveryOptionInModel(BaseModel):
    delivery_option: str = Field(...)
    specifications: Optional[str] = Field(None)

    def to_database_dict(self) -> Dict:
        result = {
            'delivery_option': self.delivery_option,
            'specifications': self.specifications,
        }
        return result
