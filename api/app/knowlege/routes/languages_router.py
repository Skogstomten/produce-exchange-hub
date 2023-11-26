# from fastapi import APIRouter, Depends
#
# from app.knowlege.datastores.language_datastore import LanguageDatastore, get_language_datastore
# from app.knowlege.models.db.language import Language
# from app.shared.config.routing_config import BASE_PATH
#
# router = APIRouter(prefix=BASE_PATH + "/languages", tags=["Language"])
#
#
# @router.get("/", response_model=list[Language])
# async def get_languages(ds: LanguageDatastore = Depends(get_language_datastore)):
#     return ds.get_languages()
