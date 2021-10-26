from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders
from app.models.companies.out_models.delivery_option_out_model import DeliveryOptionOutModel


class BuysOutModel(BaseModel):
    produce_type: str
    description: Optional[str] = Field(None)
    max_price: Optional[float] = None
    min_number_of_units: Optional[int] = None
    unit_type: Optional[str] = None
    delivery_options: List[DeliveryOptionOutModel] = []

    @classmethod
    def create(
            cls,
            data: Dict[str, str | float | int | List | Dict],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ):
        return cls(
            produce_type=datastore.localize_from_document(
                Localization.produce_types,
                data.get('produce_type'),
                headers.language,
                company_languages
            ),
            description=datastore.localize(data.get('description', None), headers.language, company_languages),
            max_price=data.get('max_price', None),
            min_number_of_units=data.get('min_number_of_units', None),
            unit_type=datastore.localize_from_document(
                Localization.unit_types,
                data.get('unit_type', None),
                headers.language,
                company_languages
            ),
            delivery_options=[
                DeliveryOptionOutModel.create(delivery_option, headers, company_languages, datastore)
                for delivery_option
                in data.get('delivery_options', [])
            ],
        )
