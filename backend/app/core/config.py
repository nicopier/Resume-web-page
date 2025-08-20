# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_NAME", "resume_app")
    DB_USER: str = os.getenv("DB_USER", "cuenta_servicio")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "cuenta_servicio")

    @property
    def DB_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 360))
    CORS_ORIGINS: str | list[str] = os.getenv("CORS_ORIGINS", "http://localhost:4200")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:4200")

settings = Settings()

#curl -X POST http://127.0.0.1:8000/auth/register ^
#  -H "Content-Type: application/json" ^
#  -d "{\"email\":\"dev@test.com\",\"password\":\"qwerty\",\"full_name\":\"Dev Test\"}"

