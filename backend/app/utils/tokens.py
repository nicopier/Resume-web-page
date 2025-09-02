# backend/app/utils/tokens.py
from __future__ import annotations

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from typing import Any, Dict

from app.core.config import settings

def _serializer(purpose: str) -> URLSafeTimedSerializer:
    """
    Crea un serializer por 'purpose' para aislar confirm/reset.
    """
    secret = settings.SECRET_KEY  # viene de .env
    return URLSafeTimedSerializer(secret_key=secret, salt=f"resume-interactivo:{purpose}")

def create_token(payload: Dict[str, Any], *, purpose: str) -> str:
    """
    Crea un token firmado (URL-safe) con un 'purpose' específico.
    Ej: purpose='email_confirm' o 'password_reset'
    """
    return _serializer(purpose).dumps(payload)

def verify_token(token: str, *, purpose: str, max_age_seconds: int) -> Dict[str, Any]:
    """
    Verifica firma + expiración. Devuelve el payload si es válido.
    Lanza ValueError si es inválido/expirado.
    """
    try:
        data = _serializer(purpose).loads(token, max_age=max_age_seconds)
        if not isinstance(data, dict):
            raise ValueError("Token payload inválido.")
        return data
    except SignatureExpired as e:
        raise ValueError("Token expirado.") from e
    except BadSignature as e:
        raise ValueError("Token inválido.") from e

# Wrappers convenientes (usan tus expiraciones en MINUTOS desde settings)
def create_email_confirm_token(user_id: int | str) -> str:
    return create_token({"sub": str(user_id)}, purpose="email_confirm")

def create_password_reset_token(user_id: int | str) -> str:
    return create_token({"sub": str(user_id)}, purpose="password_reset")

def verify_email_confirm_token(token: str) -> Dict[str, Any]:
    minutes = int(getattr(settings, "EMAIL_CONFIRM_EXPIRE_MIN", 60 * 24))
    return verify_token(token, purpose="email_confirm", max_age_seconds=minutes * 60)

def verify_password_reset_token(token: str) -> Dict[str, Any]:
    minutes = int(getattr(settings, "PASSWORD_RESET_EXPIRE_MIN", 30))
    return verify_token(token, purpose="password_reset", max_age_seconds=minutes * 60)
