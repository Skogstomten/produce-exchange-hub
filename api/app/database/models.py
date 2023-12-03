from datetime import datetime
from enum import Enum

from peewee import AutoField, CharField, BooleanField, DateTimeField, ForeignKeyField
from pytz import utc

from app.database.dependencies.orm_db import BaseModel
from app.database.enums import CompanyStatus, CompanyTypes, Language, ContactType, ChangeType, CompanyRole
from app.database.fields.enum_field import EnumField
from app.database.fields.json_field import JsonField
from app.database.fields.set_field import SetField


class User(BaseModel):
    id = AutoField(primary_key=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    firstname = CharField(null=False)
    lastname = CharField(null=False)
    password_hash = CharField(max_length=1000, null=False)
    verified = BooleanField(null=False, default=False)
    is_superuser = BooleanField(null=False, default=False)


class Company(BaseModel):
    """DB model for companies."""

    id: int = AutoField(primary_key=True)
    name: CharField = CharField(null=False)
    status: EnumField[CompanyStatus] = EnumField(CompanyStatus, default=CompanyStatus.created)
    created_date = DateTimeField(default=datetime.now(utc))
    company_types: SetField[CompanyTypes] = SetField(default=[])
    content_languages_iso = SetField(default=[Language.SV])
    activation_date = DateTimeField(null=True)
    description = JsonField(null=True)
    external_website_url: CharField = CharField(null=True)
    profile_picture_file_name = CharField(null=True)


class CompanyUser(BaseModel):
    """DB model for users connected to company and their role in connected company."""

    user_id = ForeignKeyField(User, on_delete="CASCADE", null=False)
    company_id = ForeignKeyField(Company, backref="users", on_delete="CASCADE", null=False)
    role = EnumField(CompanyRole)


class Contact(BaseModel):
    """DB model for contacts."""

    id = AutoField(primary_key=True)
    type = EnumField(ContactType)
    value = CharField(null=False)
    description = CharField(null=True)

    company = ForeignKeyField(Company, backref="contacts", on_delete="CASCADE", null=False)


class Change(BaseModel):
    """Database model for changes."""

    id = AutoField(primary_key=True)
    path = CharField(null=False)
    change_type = EnumField(ChangeType, null=False)
    actor_username = CharField(null=False)
    changed_at = DateTimeField(null=False)
    new_value = JsonField(null=False)

    company = ForeignKeyField(Company, backref="changes", on_delete="CASCADE", null=True)

    @classmethod
    def create(
        cls,
        change_id: str,
        path: str,
        change_type: ChangeType,
        username: str,
        new_value: str | int | float | datetime | dict | list | Enum | None,
    ) -> "Change":
        """
        Creates a new instance of ChangeDatabaseModel.
        :param change_id: The id to use for the change. Should be a generated id supported by the underlying database.
        :param path: Path of changed field.
        :param change_type: Type of change.
        :param username: Username of user instigating the change.
        :param new_value: The new value.
        """
        return cls(
            id=change_id,
            path=path,
            change_type=change_type,
            actor_username=username,
            changed_at=datetime.now(utc),
            new_value=new_value,
        )
