from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import companies, company_news_feed, company_addresses, company_buys, auth, users

app = FastAPI(
    dependencies=[
    ],
)
app.include_router(companies.router)
# app.include_router(company_news_feed.router)
# app.include_router(company_addresses.router)
# app.include_router(company_buys.router)
app.include_router(auth.router)
# app.include_router(users.router)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(
#     VerifyIDTokenMiddleware,
#     auth_client=Depends(get_auth_client)
# )


@app.get('/')
async def root():
    return {'message': 'This is root'}
