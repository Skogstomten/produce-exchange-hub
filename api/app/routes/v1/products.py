from fastapi import APIRouter, Body, Depends, Security

from app.datastores.product_datastore import ProductDatastore, get_product_datastore
from app.dependencies.essentials import Essentials, get_essentials
from app.dependencies.log import AppLoggerInjector, AppLogger
from app.dependencies.user import get_current_user
from app.models.v1.api_models.products import ProductOutModel, AddProductModel
from app.models.v1.database_models.user import User
from app.utils.request_utils import get_url

router = APIRouter(prefix="/v1/{lang}/products", tags=["Products"])
_logger_injector = AppLoggerInjector("products_router")


@router.post("/", response_model=ProductOutModel)
async def add_product(
    product: AddProductModel = Body(...),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
    authenticated_user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin")),
    logger: AppLogger = Depends(_logger_injector),
    essentials: Essentials = Depends(get_essentials),
):
    logger.debug(
        f"Incoming={get_url(essentials.request)}: lang={essentials.language}, product={product}, "
        f"authenticated_user={authenticated_user}"
    )
    product = product_datastore.add_product(product.name, essentials.language)
    return ProductOutModel.from_db_model(product, essentials.language)
