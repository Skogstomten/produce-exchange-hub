from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies.auth import oauth2_scheme, get_current_user
from .models.v1.user import User
from .routes import companies, auth

app = FastAPI(
    dependencies=[
    ],
)
app.include_router(companies.router)
app.include_router(auth.router)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {'message': 'This is root'}


# Security testing
@app.get('/test-auth')
def test_auth(token: str = Depends(oauth2_scheme)):
    return {'token': token}





@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
