from __future__ import annotations

from pathlib import Path

from app_paths import get_app_data_dir, get_default_backup_dir, get_default_db_path


def test_app_paths_respect_override(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("PY_SIMPLE_INVENTORY_DATA_DIR", str(tmp_path / "custom-data"))
    app_dir = get_app_data_dir()
    assert app_dir == tmp_path / "custom-data"
    assert get_default_db_path() == app_dir / "warehouse.db"
    assert get_default_backup_dir() == app_dir / "backups"
