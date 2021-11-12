from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class DeliveryOptionOutModel(BaseModel):
    delivery_option: str = Field(...)
    delivery_option_localized: Optional[str] = Field(None)
    specifications: Optional[str] = Field(None)

    @classmethod
    def create(
            cls,
            data: Dict[str, str],
            headers: AppHeaders,
            company_languages: List[str],
            datastore: BaseDatastore
    ):
        delivery_option: str = data.get('delivery_option')
        return cls(
            delivery_option=delivery_option,
            delivery_option_localized=datastore.localize_from_document(
                Localization.delivery_options,
                delivery_option,
                headers.language,
                company_languages
            ),
            specifications=data.get('specifications')
        )
