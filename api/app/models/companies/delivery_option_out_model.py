from typing import Optional, Dict, List

from pydantic import BaseModel

from app.datastores.base_datastore import BaseDatastore, Localization
from app.dependencies.app_headers import AppHeaders


class DeliveryOptionOutModel(BaseModel):
    delivery_option: str
    specifications: Optional[str] = None

    @staticmethod
    def create(data: Dict[str, str],
               headers: AppHeaders,
               company_languages: List[str],
               datastore: BaseDatastore) -> Dict:
        return {
            'delivery_option': datastore.localize_from_document(
                Localization.delivery_options,
                data.get('delivery_option'),
                headers.language,
                company_languages
            ),
            'specifications': data.get('specifications'),
        }
    