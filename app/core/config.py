from functools import lru_cache
from pathlib import Path
import os
import sys

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Quản lý kho"
    database_filename: str = os.getenv("DATABASE_FILENAME", "inventory.db")
    data_dir_name: str = os.getenv("DATA_DIR_NAME", "data")
    secret_key: str = os.getenv("SECRET_KEY", "tung-lc-invertory-app")
    auth_token_ttl_seconds: int = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", str(60 * 60 * 18)))

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def executable_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return self.project_root

    @property
    def data_dir(self) -> Path:
        return self.executable_dir / self.data_dir_name

    @property
    def database_path(self) -> Path:
        override = os.getenv("DATABASE_PATH")
        if override:
            return Path(override).resolve()
        return self.data_dir / self.database_filename

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
