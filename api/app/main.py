from fastapi import FastAPI

from .routes import root, users, token

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(token.router)
