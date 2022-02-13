from fastapi import FastAPI

from .routes import root, users, token, companies

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(companies.router)
