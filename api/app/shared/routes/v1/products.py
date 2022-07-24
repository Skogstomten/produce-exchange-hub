from fastapi import APIRouter, Body, Depends, Security, Path

from app.shared.config.routing_config import BASE_PATH
from app.shared.datastores.product_datastore import ProductDatastore, get_product_datastore
from app.shared.dependencies.essentials import Essentials, get_essentials
from app.shared.dependencies.log import AppLoggerInjector, AppLogger
from app.authentication.dependencies.user import get_current_user
from app.shared.models.v1.products import ProductOutModel, AddProductModel, ProductUpdateModel
from app.user.models.db.user import User
from app.shared.utils.request_utils import get_url

router = APIRouter(prefix=BASE_PATH + "/products", tags=["Products"])
_logger_injector = AppLoggerInjector("products_router")


@router.get("/", response_model=list[ProductOutModel])
async def get_products(
    essentials: Essentials = Depends(get_essentials),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
):
    """Get all products."""
    return await search_products(None, essentials, product_datastore)


@router.get("/{name_search}", response_model=list[ProductOutModel])
async def search_products(
    name_search: str | None = Path(None),
    essentials: Essentials = Depends(get_essentials),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
):
    """Get products matching name query."""
    products = product_datastore.get_products(essentials.language, name_search.title() if name_search else None)
    return [ProductOutModel.from_db_model(product, essentials.language) for product in products]


@router.post("/", response_model=ProductOutModel)
async def add_product(
    product: AddProductModel = Body(...),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
    authenticated_user: User = Security(get_current_user, scopes=("roles:superuser", "roles:company_admin:*")),
    logger: AppLogger = Depends(_logger_injector),
    essentials: Essentials = Depends(get_essentials),
):
    """Add new product."""
    logger.debug(
        f"Incoming={get_url(essentials.request)}: lang={essentials.language}, product={product}, "
        f"authenticated_user={authenticated_user}"
    )
    product = product_datastore.add_product(product.name, essentials.language)
    return ProductOutModel.from_db_model(product, essentials.language)


@router.put("/{product_id}", response_model=ProductOutModel)
async def update_product(
    product_id: str,
    model: ProductUpdateModel = Body(...),
    authenticated_user: User = Security(get_current_user, scopes=("roles:company_admin:*",)),
    product_datastore: ProductDatastore = Depends(get_product_datastore),
    essentials: Essentials = Depends(get_essentials),
    logger: AppLogger = Depends(_logger_injector),
):
    """Update product."""
    logger.debug(
        f"Incoming={get_url(essentials.request)}: product_id={product_id}, authenticated_user={authenticated_user}"
    )
    product = product_datastore.update_product(product_id, model.to_db_model(product_id))
    return ProductOutModel.from_db_model(product, essentials.language)
