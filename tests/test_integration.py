from __future__ import annotations

from pathlib import Path

from database.connection import DatabaseManager
from services import WarehouseService


def test_stock_consistency_invariant(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 20)
    service.export_stock("SKU1", 3)
    code = service.create_hold([{"sku": "SKU1", "quantity": 7}])
    service.finalize_hold(code, [{"sku": "SKU1", "quantity": 2}])

    mismatches = service.check_stock_consistency()
    assert mismatches == []


def test_report_matches_ledger(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 10)
    service.export_stock("SKU1", 4)

    rows = service.get_report("2000-01-01", "2099-12-31")
    row = next(r for r in rows if r["sku"] == "SKU1")
    assert row["opening"] == 0
    assert row["import"] == 10
    assert row["export"] == 4
    assert row["closing"] == 6


def test_backup_and_restore(service, tmp_path: Path):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 11)

    backup_dir = tmp_path / "backup"
    backup_file = Path(service.backup_db(backup_dir))
    assert backup_file.exists()

    db2_path = tmp_path / "restored.db"
    db2 = DatabaseManager(db2_path)
    db2.init_db()
    service2 = WarehouseService(db2)
    service2.restore_db(backup_file)

    inv = service2.get_inventory()
    assert inv[0]["sku"] == "SKU1"
    assert inv[0]["quantity"] == 11
