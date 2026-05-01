# Py Simple Inventory

Warehouse management desktop app with Python, Tkinter, SQLite.

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
