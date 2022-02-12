from fastapi import FastAPI

from .routes import root, users

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
