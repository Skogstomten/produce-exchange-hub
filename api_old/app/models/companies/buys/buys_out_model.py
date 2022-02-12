from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization, localize
from app.dependencies.app_headers import AppHeaders
from app.models.companies.buys.delivery_option_out_model import DeliveryOptionOutModel


class BuysOutModel(BaseModel):
    id: str = Field(...)
    produce_type: str = Field(...)
    produce_type_localized: Optional[str] = Field(None)
    description: Optional[Dict[str, str]] = Field({})
    description_localized: Optional[str] = Field(None)
    max_price: Optional[float] = Field(None)
    min_number_of_units: Optional[int] = Field(None)
    unit_type: Optional[str] = Field(None)
    unit_type_localized: Optional[str] = Field(None)
    delivery_options: Optional[List[DeliveryOptionOutModel]] = Field([])

    @classmethod
    def create(
            cls,
            buys_id: str,
            data: Dict[str, List[Dict[str, str]] | Dict[str, str] | float | int | str],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ):
        produce_type: str = data.get('produce_type')
        description: Dict[str, str] = data.get('description')
        unit_type: str = data.get('unit_type')
        delivery_options: List[DeliveryOptionOutModel] = []
        for delivery_option in data.get('delivery_options', []):
            delivery_options.append(
                DeliveryOptionOutModel.create(delivery_option, headers, company_languages, datastore)
            )
        return cls(
            id=buys_id,
            produce_type=produce_type,
            produce_type_localized=datastore.localize_from_document(
                Localization.produce_types,
                produce_type,
                headers.language,
                company_languages
            ),
            description=description,
            description_localized=localize(description, headers.language, company_languages),
            max_price=data.get('max_price'),
            min_number_of_units=data.get('min_number_of_units'),
            unit_type=unit_type,
            unit_type_localized=datastore.localize_from_document(
                Localization.unit_types,
                unit_type,
                headers.language,
                company_languages
            ),
            delivery_options=delivery_options
        )
