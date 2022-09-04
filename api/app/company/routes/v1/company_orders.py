from fastapi import APIRouter, Depends, Security, Body

from app.authentication.dependencies.user import get_current_user
from app.authentication.models.db.user import User
from app.company.datastores.company_datastore import get_company_datastore
from app.company.datastores.company_order_datastore import CompanyOrderDatastore
from app.company.models.v1.orders import OrderOutModel, AddOrderModel
from app.knowlege.datastores.product_datastore import ProductDatastore, get_product_datastore
from app.shared.config.routing_config import BASE_PATH
from app.shared.dependencies.essentials import Essentials, get_essentials
from app.shared.utils.lang_utils import select_localized_text

router = APIRouter(prefix=BASE_PATH + "/companies/{company_id}/orders", tags=["CompanyOrders"])


@router.post("/", response_model=OrderOutModel)
def add_order(
    company_id: str,
    new_order: AddOrderModel = Body(...),
    essentials: Essentials = Depends(get_essentials),
    authenticated_user: User = Security(get_current_user, scopes=("roles:company_admin:{company_id}",)),
    datastore: CompanyOrderDatastore = Depends(get_company_datastore),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
):
    order = datastore.add_order(company_id, new_order, authenticated_user)
    company_languages = datastore.get_company_languages(company_id)
    product_name = select_localized_text(
        product_datastore.get_product(new_order.product_id).name, essentials.language, company_languages
    )
    return OrderOutModel.from_db_model(order, product_name, essentials.language, company_languages)
