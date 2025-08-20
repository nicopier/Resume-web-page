# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Any

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    class Config:
        from_attributes = True

class LoginForm(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ResumeDocIn(BaseModel):
    locale: str
    full_name: str
    email: EmailStr
    phone: str | None = None
    location: str | None = None
    birth_date: date | None = None  # espera YYYY-MM-DD

class ResumeDocOut(BaseModel):
    id: int
    locale: str
    version: int
    is_current: bool
    data: dict[str, Any]

    class Config:
        from_attributes = True