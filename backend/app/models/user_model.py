from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import re


class UserSignup(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError(
                "Password must contain uppercase letter"
            )

        if not re.search(r"[a-z]", v):
            raise ValueError(
                "Password must contain lowercase letter"
            )

        if not re.search(r"\d", v):
            raise ValueError(
                "Password must contain number"
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError(
                "Password must contain special character"
            )

        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.lower()


class UserInDB(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = datetime.utcnow()