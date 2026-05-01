"""Application data paths for cross-platform desktop runtime."""

from __future__ import annotations

import os
import sys
from pathlib import Path

APP_DIR_NAME = "py-simple-inventory"


def get_app_data_dir() -> Path:
    override = os.getenv("PY_SIMPLE_INVENTORY_DATA_DIR")
    if override:
        path = Path(override).expanduser()
    elif sys.platform == "win32":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        path = base / APP_DIR_NAME
    elif sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / APP_DIR_NAME
    else:
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        path = base / APP_DIR_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_default_db_path() -> Path:
    return get_app_data_dir() / "warehouse.db"


def get_default_backup_dir() -> Path:
    path = get_app_data_dir() / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path
