"""Main file for application."""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .errors import ErrorModel
from .routes.v1 import (
    companies,
    token,
    users,
    timezones,
    company_contacts,
    roles,
    user_roles,
)
from .utils.request_utils import get_url

app = FastAPI(
    title="Produce Exchange Hub Api",
    description="Has all the business logic for the Produce Exchange Hub Web " "App",
)

app.include_router(users.router)
app.include_router(token.router)
app.include_router(companies.router)
app.include_router(timezones.router)
app.include_router(company_contacts.router)
app.include_router(roles.router)
app.include_router(user_roles.router)

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


@app.exception_handler(Exception)
def base_exception_handler(request: Request, err: Exception):
    """Exception handler for application."""
    if isinstance(err, HTTPException):
        return JSONResponse(
            status_code=err.status_code,
            content=ErrorModel(err.status_code, err.detail, get_url(request)).dict(),
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorModel(status.HTTP_500_INTERNAL_SERVER_ERROR, str(err), get_url(request)).dict(),
    )
