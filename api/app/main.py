from fastapi import FastAPI, Depends

from .datastores.companies_datastore import get_companies_datastore
from .dependencies.firestore import get_firebase_app, get_db_client
from .routes import companies

app = FastAPI(
    dependencies=[
        Depends(get_companies_datastore),
        Depends(get_firebase_app),
        Depends(get_db_client),
    ]
)
app.include_router(companies.router)


@app.get('/')
async def root():
    return {'message': 'This is root'}
