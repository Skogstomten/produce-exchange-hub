from fastapi import FastAPI

from .routes import root

app = FastAPI()
app.include_router(root.router)
