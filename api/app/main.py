"""Main file for application."""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .dependencies.log import AppLogger
from .errors import ErrorModel
from .routes.v1 import (
    companies,
    token,
    users,
    timezones,
    company_contacts,
    roles,
    user_roles,
    company_users,
    company_addresses,
)
from .utils.request_utils import get_url

logger = AppLogger("main")
logger.info("Application Starting...")

app = FastAPI(
    title="Produce Exchange Hub Api",
    description="Has all the business logic for the Produce Exchange Hub Web " "App",
    responses={"500": {"description": "Internal Server Error", "model": ErrorModel}},
)

app.include_router(users.router)
app.include_router(token.router)
app.include_router(companies.router)
app.include_router(timezones.router)
app.include_router(company_contacts.router)
app.include_router(roles.router)
app.include_router(user_roles.router)
app.include_router(company_users.router)
app.include_router(company_addresses.router)

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
            content=ErrorModel.create(err.status_code, err.detail, get_url(request)).dict(),
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorModel.create(status.HTTP_500_INTERNAL_SERVER_ERROR, str(err), get_url(request)).dict(),
    )


# @app.middleware("http")
# async def sla_log(request: Request, call_next):
#     """
#     Logs sla log.
#     :param request: HTTP request.
#     :param call_next: Next call to make.
#     """
#     start_time = datetime.now()
#     call_start = datetime.now(utc)
#     response: Response = await call_next(request)
#     if response.status_code not in(307, 308):
#         time_delta = datetime.now() - start_time
#         call_end = datetime.now(utc)
#     return response
