from __future__ import annotations

import pytest

from database.connection import DatabaseManager
from services import WarehouseService


def test_ui_smoke_startup(tmp_path):
    tkinter = pytest.importorskip("tkinter")

    try:
        from ui.app import WarehouseApp
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Tkinter UI unavailable: {exc}")
        return

    db = DatabaseManager(tmp_path / "ui.db")
    service = WarehouseService(db)

    try:
        app = WarehouseApp(service)
    except tkinter.TclError:
        pytest.skip("No display available for Tkinter smoke test")
        return

    app.update_idletasks()
    app.destroy()
