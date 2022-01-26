from pydantic import BaseModel, Field


class LoginModel(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
