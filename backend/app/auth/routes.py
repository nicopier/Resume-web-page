# app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import EmailStr, BaseModel
from datetime import datetime, timezone, timedelta
import os

from app.db.session import get_db
from app.db.models import User
from app.schemas import Token, LoginForm, ForgotPasswordRequest, ResetPasswordRequest
from app.auth.security import verify_password, create_access_token

# ---- Password reset helpers (tuyos) ----
from app.core.security import create_reset_token, decode_reset_token, hash_password

# ---- Confirmación de email (ajuste de imports: SIN backend.) ----
from app.utils.tokens import create_email_confirm_token, verify_email_confirm_token
from app.core.config import settings
from app.services.email_notifications import send_verify_email, send_reset_password_email
from app.schemas import Token, LoginForm, ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

# -------------------------------------------------------------------
# Registro (mismo código que estaba en main.py, sin cambios)
# -------------------------------------------------------------------

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(400, "Email ya registrado")
    u = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        provider="local",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    
    token = create_email_confirm_token(u.id)
    action_url = f"{settings.FRONTEND_URL}/auth/confirm?token={token}"
    
    send_verify_email(
        to=u.email,
        action_url=action_url,
        user_name=u.full_name or u.email.split("@")[0],
    )
    
    return u



# -------------------------------------------------------------------
# Disponibilidad de email
# -------------------------------------------------------------------
@router.get("/check-email")
def check_email(email: EmailStr, db: Session = Depends(get_db)):
    exists = db.query(User.id).filter(User.email == email).first() is not None
    return {"available": not exists}

# -------------------------------------------------------------------
# Login (bloquea si no verificó)
# -------------------------------------------------------------------
@router.post("/login", response_model=Token)
def login_json(form: LoginForm, db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == form.email)).scalar_one_or_none()
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")

    # nuevo: bloquear si no verificó
    if not getattr(u, "is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta no verificada. Revisá tu correo o reenviá el link."
        )

    return {"access_token": create_access_token(u.email), "token_type": "bearer"}

@router.post("/login-form", response_model=Token)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == form.username)).scalar_one_or_none()
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")

    if not getattr(u, "is_verified", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta no verificada. Revisá tu correo o reenviá el link."
        )

    return {"access_token": create_access_token(u.email), "token_type": "bearer"}

# -------------------------------------------------------------------
# Recuperación de contraseña
# -------------------------------------------------------------------

FORGOT_MINUTES = 5

def _build_reset_link(token: str) -> str:
    return f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}"

@router.post("/forgot-password", status_code=204)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        return  # siempre 204

    # rate-limit por email
    now = datetime.utcnow()
    last = getattr(user, "last_password_reset_sent", None)
    if last and (now - last) < timedelta(minutes=FORGOT_MINUTES):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"code": "FORGOT_RATE_LIMIT", "minutes": FORGOT_MINUTES},
            headers={"Retry-After": str(FORGOT_MINUTES * 60)},
        )

    token = create_reset_token(user_id=user.id, password_version=user.password_version)
    print("[FORGOT] token:", token[:20], "...", token[-20:])  # <-- LOG
    action_url = _build_reset_link(token)
    #
    #print("[FORGOT] url:", action_url)     
    #action_url = _build_reset_link(token)

    send_reset_password_email(
        to=user.email,
        action_url=action_url,
        user_name=user.full_name or user.email.split("@")[0],
    )

    user.last_password_reset_sent = now
    db.add(user)
    db.commit()
    return

# -------------------------------------------------------------------
# Cambiar contraseña 
# -------------------------------------------------------------------

@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    
    print("[RESET] incoming token:", (payload.token or "")[:20], "...", (payload.token or "")[-20:])
    try:
        data = decode_reset_token(payload.token)
        #print("[RESET] decoded:", {"sub": getattr(data, "sub", None), "v": getattr(data, "v", None), "exp": getattr(data, "exp", None)})
    except ValueError as e:
        #print("[RESET] decode error:", str(e))  # <-- LOG del motivo exacto
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "TOKEN_INVALID_OR_EXPIRED"}
        )
    
    
    # 1) Decodificar y validar token
    try:
        data = decode_reset_token(payload.token)  # debe traer .sub (user_id) y .v (password_version)
    except ValueError:
        # → estructura pensada para i18n en el front
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "TOKEN_INVALID_OR_EXPIRED"}
        )

    # 2) Buscar usuario por ID del token
    user = db.query(User).filter(User.id == data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "TOKEN_USER_NOT_FOUND"}
        )

    # 3) Verificar que la versión del token coincida (si no, ya caducó/ya se usó)
    if getattr(user, "password_version", 0) != getattr(data, "v", -1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "TOKEN_VERSION_MISMATCH"}  # caducado/ya usado
        )

    # 4) Guardar nueva contraseña + invalidar token(s) anteriores
    user.hashed_password = hash_password(payload.new_password)
    user.password_version = (user.password_version or 0) + 1  # ← esto caduca el código usado
    db.add(user)
    db.commit()
    return

# -------------------------------------------------------------------
# Confirmación de correo (GET /auth/confirm?token=...)
# -------------------------------------------------------------------
@router.get("/confirm")
def confirm_email(token: str = Query(..., description="Token de verificación firmado"),
                  db: Session = Depends(get_db)):
    try:
        payload = verify_email_confirm_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token sin 'sub'.")

    try:
        uid = int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido.")

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

    if getattr(user, "is_verified", False) is True:
        return {"ok": True, "user_id": str(uid), "already_verified": True}

    # marcar verificado
    if hasattr(user, "is_verified"):
        user.is_verified = True
    if hasattr(user, "verified_at"):
        user.verified_at = datetime.utcnow()

    db.add(user)
    db.commit()
    return {"ok": True, "user_id": str(uid)}

# -------------------------------------------------------------------
# Reenviar verificación (rate-limit 5 minutos)
# -------------------------------------------------------------------
RESEND_MINUTES = 5

class ResendConfirmIn(BaseModel):
    email: EmailStr

@router.post("/resend-confirm")
def resend_confirm(payload: ResendConfirmIn, db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not u:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")

    if getattr(u, "is_verified", False):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La cuenta ya está verificada")

    now = datetime.utcnow()  # tu columna es DATETIME naive en MySQL
    last = getattr(u, "last_verification_sent", None)
    if last and (now - last) < timedelta(minutes=RESEND_MINUTES):
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            f"Debes esperar {RESEND_MINUTES} minutos para reenviar"
        )

    token = create_email_confirm_token(u.id)
    action_url = f"{settings.FRONTEND_URL}/auth/confirm?token={token}"

    send_verify_email(
        to=u.email,
        action_url=action_url,
        user_name=u.full_name or u.email.split("@")[0],
    )

    u.last_verification_sent = now
    db.add(u)
    db.commit()

    return {"ok": True, "message": "Correo de verificación reenviado"}
