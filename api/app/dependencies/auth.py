from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'ee762166e05623ba6a59c9a154fe2e7fc62146756f7d5dfbc1ca888fa33f9c63'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl='token', auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
