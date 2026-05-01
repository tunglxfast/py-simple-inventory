# AGENT NOTES

## Project
- Name: `py-simple-inventory`
- Stack: Python + Tkinter + SQLite
- Goal: Desktop warehouse app for end users

## Current Scope (V1)
- Included: Products, Import, Export, Hold, Hold Management, Sales, Reports, Setup
- Setup includes: Initial stock import (Excel/CSV), Reset database, Backup/Restore
- Excluded in this phase: Stock Audit, Snapshot/Comparison

## Core Data Rules
- `ledger` is source of truth for stock movements.
- Every stock change must create a ledger entry.
- `products.quantity` must remain consistent with ledger sum.
- Sale record is business output; stock effect is handled by export/return movements.

## Architecture
- `database/`: schema + connection + transaction helper
- `services/`: business logic (no UI SQL)
- `ui/`: Tkinter screens + i18n
- `tests/`: unit + integration + smoke
- Entrypoint: `app.py`

## Important Operational Notes
- Transactions required for all write operations.
- Enforce validation: quantity > 0, no negative stock, return <= held quantity.
- Keep historical transaction integrity; avoid editing/deleting ledger records.

## Packaging Direction
- Preferred packager: PyInstaller.
- Before release build:
  - Move DB path to user-data directory (not working directory / install directory).
  - Verify optional `openpyxl` inclusion in packaged app.
  - Add build scripts/spec for reproducible output.
