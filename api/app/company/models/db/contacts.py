"""ContactDatabaseModel."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pytz import utc
from sqlalchemy import Enum, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.company.models.shared.enums import ContactType
from app.database.dependencies.mysql import BaseModel


class Contact(BaseModel):
    """DB model for contacts."""

    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[ContactType] = mapped_column(Enum(ContactType))
    value: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    created_by: Mapped[str] = mapped_column(String(100), default="MISSING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(utc))
    changed_by: Mapped[Optional[str]] = mapped_column(String(100))
    changed_at: Mapped[Optional[datetime]]
