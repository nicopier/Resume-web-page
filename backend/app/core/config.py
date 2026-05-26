# app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ruta absoluta al .env en la raíz del repo
ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".env"

class Settings(BaseSettings):
    # ---- DB ----
    # Render provee DATABASE_URL directamente; en local usamos los campos individuales
    DATABASE_URL: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "resume_app"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    @property
    def DB_URL(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            # Render usa postgres:// pero psycopg2 necesita postgresql+psycopg2://
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+psycopg2://", 1)
            elif url.startswith("postgresql://") and "+psycopg2" not in url:
                url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
            return url
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # ---- Seguridad / Tokens ----
    SECRET_KEY: str = "dev-secret-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 360
    EMAIL_CONFIRM_EXPIRE_MIN: int = 60 * 24
    PASSWORD_RESET_EXPIRE_MIN: int = 30

    # ---- Frontend / CORS ----
    CORS_ORIGINS: str | list[str] = "http://localhost:4200"
    FRONTEND_URL: str = "http://localhost:4200"
    FRONTEND_BASE_URL: str = "http://localhost:4200"

    # ---- Gmail ----
    # 👉 con defaults para no romper si faltan
    GMAIL_USER: str = ""
    GMAIL_APP_PASSWORD: str = ""
    EMAIL_FROM_NAME: str = "Resume Interactivo"

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",  # 👈 ignora cualquier otra clave en .env
    )




settings = Settings()


