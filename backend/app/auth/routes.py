# app/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import EmailStr

from app.db.session import get_db
from app.db.models import User
from app.schemas import Token, LoginForm
from app.auth.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/check-email")
def check_email(email: EmailStr, db: Session = Depends(get_db)):
    exists = db.query(User.id).filter(User.email == email).first() is not None
    return {"available": not exists}

@router.post("/login", response_model=Token)
def login_json(form: LoginForm, db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == form.email)).scalar_one_or_none()
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    return {"access_token": create_access_token(u.email), "token_type": "bearer"}

# (opcional) si mantenés el OAuth2 form:
@router.post("/login-form", response_model=Token)
def login_form(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.execute(select(User).where(User.email == form.username)).scalar_one_or_none()
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    return {"access_token": create_access_token(u.email), "token_type": "bearer"}
