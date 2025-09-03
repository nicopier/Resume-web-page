from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, JSON, func, ForeignKey, UniqueConstraint, Index, Boolean, text

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Enum en SQLAlchemy (coincide con tu ENUM de MySQL)
    provider: Mapped[str | None] = mapped_column(String(50), default="local", nullable=True)

    #NUEVO: versión de contraseña
    password_version: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    # Verificación de email
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("0"))
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_verification_sent: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_password_reset_sent:  Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    resumes: Mapped[list["ResumeDoc"]] = relationship(
        "ResumeDoc",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class ResumeDoc(Base):
    __tablename__ = "resume_docs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    locale: Mapped[str] = mapped_column(String(8), nullable=False, unique=False, index=True, default="en")
    
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    data: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    # --- ResumeDoc ---
    user: Mapped["User"] = relationship(
        "User",
        back_populates="resumes"
    )
    
    __table_args__ = (
        #this makes user_id locale and is_current combination repeated
        UniqueConstraint("user_id", "locale", "is_current", name="uq_user_locale_current"),
        Index("ix_user_locale_version", "user_id", "locale", "version"),
    )