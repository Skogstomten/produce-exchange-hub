# from fastapi import APIRouter, Depends
#
# from app.knowlege.datastores.country_datastore import get_country_datastore, CountryDatastore
# from app.knowlege.models.db.country import Country
# from app.shared.config.routing_config import BASE_PATH
#
# router = APIRouter(prefix=BASE_PATH + "/countries", tags=["Country"])
#
#
# @router.get("/", response_model=list[Country])
# async def get_countries(ds: CountryDatastore = Depends(get_country_datastore)):
#     return ds.get_countries()
