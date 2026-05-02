from __future__ import annotations

from app_paths import get_default_db_path
from database.connection import DatabaseManager
from services import WarehouseService
from ui_qt import run_qt_app


def main() -> int:
    db = DatabaseManager(get_default_db_path())
    service = WarehouseService(db)
    return run_qt_app(service)


if __name__ == "__main__":
    raise SystemExit(main())
