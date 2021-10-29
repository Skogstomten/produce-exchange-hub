from fastapi import FastAPI

from .routes import companies, company_news_feed, company_addresses, company_buys

app = FastAPI(
    dependencies=[
    ]
)
app.include_router(companies.router)
app.include_router(company_news_feed.router)
app.include_router(company_addresses.router)
app.include_router(company_buys.router)


@app.get('/')
async def root():
    return {'message': 'This is root'}
