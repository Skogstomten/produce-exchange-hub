from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
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


@app.exception_handler(Exception)
def base_exception_handler(request: Request, err: Exception):
    if isinstance(err, HTTPException):
        return JSONResponse(
            status_code=err.status_code,
            content={
                'status': err.status_code,
                'detail': err.detail,
            }
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'detail': str(err)
        }
    )
