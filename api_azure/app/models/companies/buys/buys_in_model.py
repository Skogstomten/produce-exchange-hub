from typing import Optional, Dict, List

from pydantic import BaseModel, Field

from .delivery_option_in_model import DeliveryOptionInModel


class BuysInModel(BaseModel):
    produce_type: str = Field(...)
    description: Optional[Dict[str, str]] = Field({})
    max_price: Optional[float] = Field(None)
    min_number_of_units: Optional[int] = Field(None)
    unit_type: Optional[str] = Field(None)
    delivery_options: Optional[List[DeliveryOptionInModel]] = Field([])

    def to_database_dict(self) -> Dict:
        result = {
            'produce_type': self.produce_type,
            'description': self.description,
            'max_price': self.max_price,
            'min_number_of_units': self.min_number_of_units,
            'unit_type': self.unit_type,
            'delivery_options': [
                delivery_option.to_database_dict()
                for delivery_option
                in self.delivery_options
            ],
        }
        return result
