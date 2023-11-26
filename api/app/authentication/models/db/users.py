from uuid import UUID

from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from app.database.dependencies.mysql import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200))
    firstname: Mapped[str] = mapped_column(String(100))
    lastname: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(1000))
    verified: Mapped[bool] = mapped_column(Boolean)
