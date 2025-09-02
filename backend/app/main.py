from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.services.email_notifications import send_verify_email
from app.core.config import settings
from app.db.session import get_db
from app.db.models import User
from app.schemas import UserCreate, UserOut, LoginForm, Token
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth import routes as auth_routes
from app.resume import routes as resume_routes

app = FastAPI(title="Resume Auth API")

# CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/auth/register", response_model=UserOut)
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
    
    action_url = f"{settings.FRONTEND_BASE_URL}/verify-email?email={u.email}"
    send_verify_email(
        to=u.email,
        action_url=action_url,
        user_name=u.full_name or u.email.split("@")[0],
    )
    
    return u

app.include_router(auth_routes.router)
app.include_router(resume_routes.router)

