from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
JWT_ALG = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

class ResetTokenData(BaseModel):
    sub: int   # user_id
    typ: str   # "reset"
    v: int     # password_version
    exp: int   # epoch seconds
    iat: int   # epoch seconds

def create_reset_token(*, user_id: int, password_version: int, minutes: Optional[int] = None) -> str:
    exp_minutes = minutes if minutes is not None else settings.PASSWORD_RESET_EXPIRE_MIN
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=exp_minutes)
    payload = {
        "sub": str(user_id),
        "typ": "reset",
        "v": int(password_version or 0),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALG)

def decode_reset_token(token: str) -> ResetTokenData:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALG],
            options={"verify_aud": False, "verify_exp": True},
        )
        data = ResetTokenData(**payload)
        if data.typ != "reset":
            raise JWTError("Invalid token type")
        return data
    except ExpiredSignatureError:
        raise ValueError("expired")
    except JWTError as e:
        raise ValueError(f"invalid: {str(e)}")
