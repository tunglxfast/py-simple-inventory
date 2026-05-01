from __future__ import annotations

from pathlib import Path

import pytest

from database.connection import DatabaseManager
from services import WarehouseService


@pytest.fixture
def service(tmp_path: Path) -> WarehouseService:
    db_path = tmp_path / "test_warehouse.db"
    db = DatabaseManager(db_path)
    return WarehouseService(db)
