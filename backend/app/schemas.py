# app/schemas.py
from pydantic import BaseModel, EmailStr, model_validator, Field
from datetime import date
from typing import Any, ClassVar
from datetime import datetime   # ← importante



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
    data: dict[str, Any]

    # definimos las claves requeridas dentro de la clase
    MAIN_KEYS: ClassVar[set[str]] = {
        "informacion_personal", 
        "introduccion", 
        "estudios", 
        "experiencia", 
        "skills"
    }

    @model_validator(mode="after")
    def _check_main_keys(self):
        d = self.data or {}
        faltan = [k for k in self.MAIN_KEYS if k not in d]
        if faltan:
            raise ValueError(f"Faltan secciones requeridas: {', '.join(faltan)}")

        if not isinstance(d["informacion_personal"], dict):
            raise ValueError("informacion_personal debe ser objeto")
        if not isinstance(d["introduccion"], dict):
            raise ValueError("introduccion debe ser objeto")
        if not isinstance(d["estudios"], list):
            raise ValueError("estudios debe ser lista")
        if not isinstance(d["experiencia"], list):
            raise ValueError("experiencia debe ser lista")
        if not isinstance(d["skills"], list):
            raise ValueError("skills debe ser lista")

        return self

class ResumeDocOut(BaseModel):
    id: int
    locale: str
    version: int
    is_current: bool
    data: dict[str, Any]

    class Config:
        from_attributes = True
        

class ResumeOut(BaseModel):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True
        
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=10)
    new_password: str = Field(..., min_length=8, max_length=128)        