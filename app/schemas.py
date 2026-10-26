
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    display_name: str = Field(min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = None
    status: Literal["active", "inactive"] = "active"

    @field_validator("display_name")
    @classmethod
    def display_name_must_not_be_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Display name must not be blank.")
        return value


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    display_name: str
    phone: str | None
    email: str | None
    status: str
    created_at: datetime


class AirlineCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    code: str = Field(min_length=2, max_length=3, pattern=r"^[A-Z0-9]{2,3}$")
    name: str = Field(min_length=1, max_length=200)
    status: Literal["active", "inactive"] = "active"

    @field_validator("code", mode="before")
    @classmethod
    def normalize_code(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Airline name must not be blank.")
        return value


class AirlineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    status: str
