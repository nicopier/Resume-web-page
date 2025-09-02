from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
import jwt

from app.db.session import get_db
from app.db.models import User, ResumeDoc
from app.schemas import ResumeDocIn, ResumeDocOut, ResumeOut
from app.core.config import settings  # SECRET_KEY

from typing import List

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
    d = body.data or {}

    # 1) validar presencia de secciones (paso a paso)
    required = {"informacion_personal", "introduccion", "estudios", "experiencia", "skills"}
    missing = [k for k in required if k not in d]
    if missing:
        raise HTTPException(status_code=422, detail=f"Faltan secciones: {', '.join(missing)}")

    # 2) tipos básicos (sin meternos adentro)
    if not isinstance(d["informacion_personal"], dict): raise HTTPException(422, "informacion_personal debe ser objeto")
    if not isinstance(d["introduccion"], dict):         raise HTTPException(422, "introduccion debe ser objeto")
    if not isinstance(d["estudios"], list):             raise HTTPException(422, "estudios debe ser lista")
    if not isinstance(d["experiencia"], list):          raise HTTPException(422, "experiencia debe ser lista")
    if not isinstance(d["skills"], list):               raise HTTPException(422, "skills debe ser lista")

    # 3) extraer locale desde el JSON
    ip = d["informacion_personal"]
    locale = str(ip.get("locale", "")).lower()[:8]
    if not locale:
        raise HTTPException(status_code=422, detail="informacion_personal.locale es requerido")

    # 4) versionado + is_current
    last_version = db.execute(
        select(func.max(ResumeDoc.version)).where(
            ResumeDoc.user_id == current.id,
            ResumeDoc.locale == locale
        )
    ).scalar() or 0
    next_version = last_version + 1

    db.execute(
        update(ResumeDoc)
        .where(
            ResumeDoc.user_id == current.id,
            ResumeDoc.locale == locale,
            ResumeDoc.is_current == True
        )
        .values(is_current=False)
    )

    # 5) guardar JSON COMPLETO
    doc = ResumeDoc(
        user_id=current.id,
        locale=locale,
        version=next_version,
        is_current=True,
        data=d,
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


@router.get("/me", response_model=List[ResumeOut])
def list_my_resumes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (
        db.query(ResumeDoc)
          .filter(ResumeDoc.user_id == user.id)
          .order_by(ResumeDoc.updated_at.desc())
          .all()
    )
    # ← casteamos a date() para que no explote el schema si espera date
    return [
        {"id": r.id, "updated_at": (r.updated_at.date() if r.updated_at else None)}
        for r in rows
    ]

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Solo permitimos borrar resumes del usuario logueado
    r = db.query(ResumeDoc).filter(
        ResumeDoc.id == resume_id,
        ResumeDoc.user_id == user.id
    ).first()

    if not r:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(r)
    db.commit()
    # 204 No Content → no devolver body