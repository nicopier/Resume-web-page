# backend/app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

# ========= Config desde .env =========
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")     # cargado desde backend/.env
JWT_ALG = os.getenv("JWT_ALG", "HS256")
RESET_TOKEN_MINUTES = int(os.getenv("RESET_TOKEN_MINUTES", "30"))

# ========= Password hashing =========
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """Devuelve el hash bcrypt para guardar en User.hashed_password"""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica una contraseña en texto plano contra el hash guardado"""
    return pwd_context.verify(plain, hashed)

# ========= Reset JWT =========
class ResetTokenData(BaseModel):
    sub: int   # user_id
    typ: str   # "reset"
    v: int     # password_version
    exp: int   # epoch seconds
    iat: int   # epoch seconds

def create_reset_token(*, user_id: int, password_version: int, minutes: Optional[int] = None) -> str:
    """Crea un JWT de reseteo con expiración corta y la versión de contraseña actual."""
    exp_minutes = minutes or RESET_TOKEN_MINUTES
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=exp_minutes)
    payload = {
        "sub": user_id,
        "typ": "reset",
        "v": password_version,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)

def decode_reset_token(token: str) -> ResetTokenData:
    """Valida/decodifica el JWT; levanta ValueError si es inválido o expiró."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALG])
        data = ResetTokenData(**payload)
        if data.typ != "reset":
            raise JWTError("Invalid token type")
        return data
    except JWTError as e:
        raise ValueError(f"Invalid reset token: {str(e)}")
