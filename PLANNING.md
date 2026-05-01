# PLANNING

## Status
- Branch: `init_basic_core`
- Baseline: aligned with `main` at start of implementation
- Core V1 implementation: completed
- Test status: `15 passed, 1 skipped` (UI smoke skipped when Tk unavailable)

## Completed Work
- Project skeleton created (`database/`, `services/`, `ui/`, `tests/`)
- SQLite schema with constraints and indexes
- Service layer for product/stock/hold/sales/report/setup
- Tkinter bilingual UI (VI/EN) with sidebar navigation
- Tests for core logic + integration + UI smoke

## Next Phase (Packaging Hardening)
1. App data path standardization (DONE)
- DB path moved to OS user-data directory via `app_paths.py`.
- Backup default path moved to user-data `backups/`.

2. Packaging setup (DONE)
- Added PyInstaller spec: `packaging/py-simple-inventory.spec`.
- Added build scripts: `scripts/build_pyinstaller.sh` and `.bat`.
- Included `openpyxl` hidden imports for packaged Excel support.

3. Release QA (NEXT)
- Smoke test packaged app flow: Products -> Import/Export -> Hold -> Sales -> Reports -> Setup.
- Validate backup/restore and initial import behavior in packaged runtime.

## Risks / Notes
- Runtime without Tk support cannot execute real UI tests.
- `.xlsx` import requires `openpyxl`; fallback CSV path remains available.

## Reference
- Project init requirement and structure: WAREHOUSE_APP_SPEC.md 
