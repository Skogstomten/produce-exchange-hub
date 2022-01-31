from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
    disabled: bool = False


def fake_decode_token(token: str) -> User:
    return User(
        id=token,
        email='serialundead@gmail.com',
        firstname='Nisse',
        lastname='Persson',
        disabled=False
    )
