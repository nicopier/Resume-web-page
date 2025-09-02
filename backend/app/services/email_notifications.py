# backend/app/services/email_notifications.py
from __future__ import annotations
from pathlib import Path
from typing import Optional, Dict

from app.utils.email_sender import EmailSender
from app.core.config import settings  # lee .env

APP_NAME: str = getattr(settings, "EMAIL_FROM_NAME", "resumeinterctivo")
EMAIL_CONFIRM_EXPIRE_MIN: int = int(getattr(settings, "EMAIL_CONFIRM_EXPIRE_MIN", 60 * 24))
PASSWORD_RESET_EXPIRE_MIN: int = int(getattr(settings, "PASSWORD_RESET_EXPIRE_MIN", 30))

# ⛔️ OJO: los templates están en app/templates/email, NO en services/templates/email
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates" / "email"

def _render_template(filename: str, context: Dict[str, object]) -> str:
    html_path = TEMPLATES_DIR / filename
    if not html_path.exists():
        raise FileNotFoundError(f"No encontré el template en: {html_path}")
    html = html_path.read_text(encoding="utf-8")
    for k, v in context.items():
        html = html.replace(f"{{{{ {k} }}}}", str(v))
    return html

def _get_sender() -> EmailSender:
    # ✅ crear el sender al momento de usarlo (evita None)
    if not settings.GMAIL_USER or not settings.GMAIL_APP_PASSWORD:
        raise RuntimeError("Faltan GMAIL_USER o GMAIL_APP_PASSWORD en .env")
    return EmailSender(
        gmail_user=settings.GMAIL_USER,
        app_password=settings.GMAIL_APP_PASSWORD,
        from_name=getattr(settings, "EMAIL_FROM_NAME", APP_NAME),
    )

def send_verify_email(
    to: str,
    action_url: str,
    user_name: str,
    *,
    app_name: Optional[str] = None,
    expire_minutes: Optional[int] = None,
    sender: Optional[EmailSender] = None,
) -> None:
    html = _render_template(
        "verify_account.html",
        {
            "user_name": user_name,
            "app_name": app_name or APP_NAME,
            "action_url": action_url,
            "expire_minutes": expire_minutes or EMAIL_CONFIRM_EXPIRE_MIN,
            "year": 2025,
        },
    )
    (sender or _get_sender()).send_html(
        to=to,
        subject=f"[{app_name or APP_NAME}] Verificá tu correo",
        html=html,
    )

def send_reset_password_email(
    to: str,
    action_url: str,
    user_name: str,
    *,
    app_name: Optional[str] = None,
    expire_minutes: Optional[int] = None,
    sender: Optional[EmailSender] = None,
) -> None:
    html = _render_template(
        "reset_password.html",
        {
            "user_name": user_name,
            "app_name": app_name or APP_NAME,
            "action_url": action_url,
            "expire_minutes": expire_minutes or PASSWORD_RESET_EXPIRE_MIN,
            "year": 2025,
        },
    )
    (sender or _get_sender()).send_html(
        to=to,
        subject=f"[{app_name or APP_NAME}] Restablecé tu contraseña",
        html=html,
    )
