# app/auth/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"

def hash_password(p: str) -> str:
    return pwd.hash(p)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd.verify(plain, hashed)

def create_access_token(subject: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": exp}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)


# Para los docs/Swagger; nuestro login real puede ser JSON,
# pero este esquema sólo define de dónde saldría el token en teoría.
