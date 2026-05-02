# Py Simple Inventory

Warehouse management desktop app with Python, Tkinter, SQLite.
Project now includes a parallel PySide6 UI migration path.

## Data location

- Database path is OS user-data based (not current working directory):
  - macOS: `~/Library/Application Support/py-simple-inventory/warehouse.db`
  - Windows: `%APPDATA%\\py-simple-inventory\\warehouse.db`
  - Linux: `$XDG_DATA_HOME/py-simple-inventory/warehouse.db` (or `~/.local/share/...`)
- You can override with env var: `PY_SIMPLE_INVENTORY_DATA_DIR`.

## Run

```bash
python3 app.py
```

PySide6 UI (new):

```bash
uv pip install -e ".[gui]"
uv run python app_qt.py
```

## Test

```bash
uv run pytest
```

## Excel support

For `.xlsx` initial stock import:

```bash
pip install ".[excel]"
```

Without `openpyxl`, the setup screen still supports `.csv` with the same columns.

## Build for end users (PyInstaller)

```bash
./scripts/build_pyinstaller.sh
```

Windows:

```bat
scripts\\build_pyinstaller.bat
```

Output binary is generated in `dist/PySimpleInventory`.

## PySide6 Migration Status

- Added `app_qt.py` entrypoint and `ui_qt/` package.
- Implemented functional pages in Qt:
  - Products (create/update + inventory table)
  - Import / Export movement form (`QSpinBox` for quantity)
  - Hold creation (table-based SKU/Quantity input)
  - Hold management (session list + return quantity editor + finalize)
  - Sales list table
  - Reports with `QDateEdit` date inputs + inventory/summary tables
  - Setup with preview/import/reset/backup/restore flows
- Added restore/reset/finalize confirmation dialogs in Qt flow.
- Kept original Tkinter app intact for fallback during migration.

## Additional Docs

- UI quick usage: `docs/UI_QUICKSTART.md`
- Build + GitHub release guide: `docs/RELEASE_PYINSTALLER.md`
