from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./QRKotData.db'
    secret: str = 'mysecret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
