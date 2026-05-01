from __future__ import annotations

from app_paths import get_default_db_path
from database.connection import DatabaseManager
from services import WarehouseService
from ui.app import WarehouseApp


def main() -> None:
    db = DatabaseManager(get_default_db_path())
    service = WarehouseService(db)
    app = WarehouseApp(service)
    app.mainloop()


if __name__ == "__main__":
    main()
