from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
import jwt

from app.db.session import get_db
from app.db.models import User, ResumeDoc
from app.schemas import ResumeDocIn, ResumeDocOut
from app.core.config import settings  # SECRET_KEY

router = APIRouter(prefix="/resume", tags=["resume"])

# --- auth helper: obtener usuario por token ---
def get_current_user(db: Session = Depends(get_db), authorization: str | None = Header(None)) -> User:
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing Authorization header")
    try:
        scheme, token = authorization.split()
        assert scheme.lower() == "bearer"
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise ValueError("no sub")
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user

# --- crear nueva versión de ResumeDoc (data JSON) ---
@router.post("", response_model=ResumeDocOut, status_code=201)
def create_resume_doc(
    body: ResumeDocIn,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    # calcular próxima versión para ese (user, locale)
    last_version = db.execute(
        select(func.max(ResumeDoc.version)).where(
            ResumeDoc.user_id == current.id,
            ResumeDoc.locale == body.locale
        )
    ).scalar() or 0
    next_version = last_version + 1

    # marcar como no-current la actual (si la hay)
    db.execute(
        update(ResumeDoc)
        .where(
            ResumeDoc.user_id == current.id,
            ResumeDoc.locale == body.locale,
            ResumeDoc.is_current == True
        )
        .values(is_current=False)
    )

    # armar data JSON desde el body
    data = {
        "full_name": body.full_name,
        "email": str(body.email),
        "phone": body.phone,
        "location": body.location,
        "birth_date": body.birth_date.isoformat() if body.birth_date else None,
    }

    doc = ResumeDoc(
        user_id=current.id,
        locale=body.locale,
        version=next_version,
        is_current=True,
        data=data,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

# (opcional) obtener la versión vigente
@router.get("/current/{locale}", response_model=ResumeDocOut)
def get_current_resume(locale: str, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    doc = db.execute(
        select(ResumeDoc).where(
            ResumeDoc.user_id == current.id,
            ResumeDoc.locale == locale,
            ResumeDoc.is_current == True
        )
    ).scalar_one_or_none()
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No resume for this locale")
    return doc
