"""CompanyDatabaseModel"""
from datetime import datetime
from typing import List, Dict
from uuid import UUID

from pytz import utc
from sqlalchemy import String, Enum, DateTime, ARRAY
from sqlalchemy.orm import mapped_column, Mapped

from app.database.dependencies.mysql import BaseModel
from app.shared.models.v1.shared import Language
from ..shared.enums import CompanyStatus, CompanyTypes


class Company(BaseModel):
    """DB model for companies."""

    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[CompanyStatus] = mapped_column(Enum(CompanyStatus), nullable=False, default=CompanyStatus.created)
    created_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(utc))
    company_types: Mapped[List[CompanyTypes]] = mapped_column(ARRAY(Enum(CompanyTypes)))
    content_languages_iso: Mapped[List[Language]] = mapped_column(ARRAY(Enum(Language)))
    activation_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    description: Mapped[Dict[Language, str]] = mapped_column(nullable=True)
    external_website_url: Mapped[str] = mapped_column(String(200), nullable=True)
