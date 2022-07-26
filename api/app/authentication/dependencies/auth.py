"""
Basic db dependency variables and constants.
"""
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "ee762166e05623ba6a59c9a154fe2e7fc62146756f7d5dfbc1ca888fa33f9c63"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OAUTH2_SCHEME_OPTIONAL = OAuth2PasswordBearer(
    tokenUrl="v1/token",
    auto_error=False,
    scopes={
        "roles": "Get user roles",
        "profile": "Include user information",
    },
)
