from typing import Dict, List, Optional

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization


class ProducesOutModel(BaseModel):
    produce_type: str
    description: Optional[str] = None
    price_per_unit: Optional[float] = None
    unit_type: Optional[str] = None
    units_per_period: Optional[int] = None
    period_type: Optional[str] = None
    delivery_options: List[DeliveryOptionOutModel]

    @staticmethod
    def create(
            data: Dict[str, List | Dict | float | int | str],
            language: str,
            company_languages: List[str],
            datastore: BaseDatastore
    ) -> Dict:
        return {
            'produce_type': datastore.localize_from_document(
                Localization.produce_types,
                data.get('produce_type'),
                language,
                company_languages
            ),
            'description': data.get('description', None),
            'price_per_unit': data.get('price_per_unit', None),
            'unit_type': datastore.localize_from_document(
                Localization.unit_types,
                data.get('unit_type', None),
                language,
                company_languages
            ),
            'units_per_period': data.get('units_per_period', None),
            'period_type': datastore.localize_from_document(
                Localization.period_types,
                data.get('period_type', None),
                language,
                company_languages
            ),
            'delivery_options': [
                DeliveryOptionOutModel.create(
                    delivery_option,
                    language,
                    company_languages,
                    datastore
                )
                for delivery_option
                in data.get('delivery_options', [])
            ],
        }
