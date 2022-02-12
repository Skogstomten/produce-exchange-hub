from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from starlette.types import ASGIApp
from firebase_admin.auth import Client


class VerifyIDTokenMiddleware(BaseHTTPMiddleware):
    auth_client: Client

    def __init__(
            self,
            app: ASGIApp,
            auth_client: Client
    ):
        super().__init__(app)
        self.auth_client = auth_client

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        pass
