from typing import List, Optional, Dict

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization
from app.models.companies.delivery_option_out_model import DeliveryOptionOutModel


class BuysOutModel(BaseModel):
    produce_type: str
    description: Optional[str] = None
    max_price: Optional[float] = None
    min_number_of_units: Optional[int] = None
    unit_type: Optional[str] = None
    delivery_options: List[DeliveryOptionOutModel] = []

    @staticmethod
    def create(data: Dict[str, str | float | int | List | Dict],
               language: str,
               company_languages: List[str],
               datastore: BaseDatastore) -> Dict:
        return {
            'produce_type': datastore.localize_from_document(Localization.produce_types,
                                                             data.get('produce_type'),
                                                             language,
                                                             company_languages).
            'description': data.get('description', None),
            'max_price': data.get('max_price', None),
            'min_number_of_units': data.get('min_number_of_units', None),
            'unit_type': datastore.localize_from_document(Localization.unit_types,
                                                          data.get('unit_type', None),
                                                          language,
                                                          company_languages),
            'delivery_options': [DeliveryOptionOutModel.create(delivery_option,
                                                               language,
                                                               company_languages,
                                                               datastore)
                                 for delivery_option
                                 in data.get('delivery_options', [])],
        }
