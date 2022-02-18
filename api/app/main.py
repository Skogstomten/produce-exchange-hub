from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import root, users, token, companies

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(companies.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
