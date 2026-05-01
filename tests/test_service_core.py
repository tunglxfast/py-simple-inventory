from __future__ import annotations

import csv
from pathlib import Path

import pytest

from services import InsufficientStockError, ValidationError


def test_import_and_export_update_stock_and_ledger(service):
    service.create_product("SKU1", "Item 1", "pcs")

    service.import_stock("SKU1", 10)
    service.export_stock("SKU1", 4)

    inv = service.get_inventory()
    assert inv[0]["quantity"] == 6

    with service.db.connection() as conn:
        ledger = conn.execute("SELECT change, type, ref_type FROM ledger WHERE sku='SKU1' ORDER BY id").fetchall()
    assert [(r["change"], r["type"], r["ref_type"]) for r in ledger] == [
        (10, "IMPORT", "IMPORT"),
        (-4, "EXPORT", "EXPORT"),
    ]


def test_export_blocked_when_stock_insufficient(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 2)

    with pytest.raises(InsufficientStockError):
        service.export_stock("SKU1", 3)


def test_hold_return_all_keeps_stock_unchanged(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 10)

    hold_code = service.create_hold([{"sku": "SKU1", "quantity": 5}])
    service.finalize_hold(hold_code, [{"sku": "SKU1", "quantity": 5}])

    inv = service.get_inventory()
    assert inv[0]["quantity"] == 10


def test_hold_partial_return_updates_stock_correctly(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 10)

    hold_code = service.create_hold([{"sku": "SKU1", "quantity": 7}])
    service.finalize_hold(hold_code, [{"sku": "SKU1", "quantity": 2}])

    inv = service.get_inventory()
    assert inv[0]["quantity"] == 5

    sales = service.get_sales()
    assert sales[0]["items"][0]["quantity"] == 5


def test_initial_import_blocked_when_stock_exists(service, tmp_path: Path):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 2)

    csv_path = tmp_path / "initial.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["MÃ HÀNG", "TÊN HÀNG HÓA", "ĐVT", "TỒN"])
        writer.writerow(["SKU2", "Item 2", "pcs", 5])

    with pytest.raises(ValidationError):
        service.import_initial_stock_from_excel(csv_path)


def test_reset_full_clears_db(service):
    service.create_product("SKU1", "Item 1", "pcs")
    service.import_stock("SKU1", 5)

    service.reset_database(mode="full", confirm_token="RESET")

    assert service.get_inventory() == []
    with service.db.connection() as conn:
        ledger_count = conn.execute("SELECT COUNT(*) AS c FROM ledger").fetchone()["c"]
    assert ledger_count == 0
