from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routes.v1 import companies, token, root, users, timezones, company_contacts
from .errors.error_model import ErrorModel
from .errors.not_found_error import NotFoundError

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(companies.router)
app.include_router(timezones.router)
app.include_router(company_contacts.router)

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
    if isinstance(err, HTTPException):
        return JSONResponse(
            status_code=err.status_code,
            content=vars(
                ErrorModel(
                    err.status_code,
                    err.detail
                )
            )
        )
    if isinstance(err, NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=vars(
                ErrorModel(
                    status.HTTP_404_NOT_FOUND,
                    f"No resource found at '{request.url.path}'"
                )
            )
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=vars(
            ErrorModel(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                str(err)
            )
        )
    )
