import logging
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"
    LOG_LEVEL: int = logging.INFO
    LOG_NAME: str = "fastapi_template"
    PROJECT_NAME: str = "FastApi template"
    LOCAL_EMAIL_ADMIN: str = "augustin.hourlier@devoteamgcloud.com"

    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:5174"]

    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:postgres@localhost:5432/fastapi_template"
    MAX_PAGE_SIZE: int = 100

    GITHUB_ACCESS_TOKEN: Optional[str] = None
    GCLOUD_PROJECT_ID: Optional[str] = "sandbox-ahourlier"

    class ConfigDict:
        env_file = ".env"


settings = Settings()
