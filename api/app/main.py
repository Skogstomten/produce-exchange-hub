from fastapi import FastAPI, Depends

from .datastores.addresses_datastore import get_addresses_datastore
from .datastores.companies_datastore import get_companies_datastore
from .datastores.news_feed_datastore import get_news_feed_datastore
from .dependencies.app_headers import get_headers
from .dependencies.firestore import get_firebase_app, get_db_client
from .routes import companies, company_news_feed, company_addresses

app = FastAPI(
    dependencies=[
        Depends(get_companies_datastore),
        Depends(get_news_feed_datastore),
        Depends(get_addresses_datastore),
        Depends(get_firebase_app),
        Depends(get_db_client),
        Depends(get_headers),
    ]
)
app.include_router(companies.router)
app.include_router(company_news_feed.router)
app.include_router(company_addresses.router)


@app.get('/')
async def root():
    return {'message': 'This is root'}
