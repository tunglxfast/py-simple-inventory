# PLANNING

## Status
- Branch: `init_basic_core`
- Baseline: aligned with `main` at start of implementation
- Core V1 implementation: completed
- Test status: `15 passed, 1 skipped` (UI smoke skipped when Tk unavailable)
- PySide6 migration: Phase 1 + core functional pages completed (parallel UI path)

## Completed Work
- Project skeleton created (`database/`, `services/`, `ui/`, `tests/`)
- SQLite schema with constraints and indexes
- Service layer for product/stock/hold/sales/report/setup
- Tkinter bilingual UI (VI/EN) with sidebar navigation
- Tests for core logic + integration + UI smoke
- Added PySide6 entrypoint (`app_qt.py`) and package (`ui_qt/`)
- Implemented Qt pages with live service wiring:
  - Products CRUD + inventory table
  - Import/Export movement forms with numeric guardrails
  - Hold creation table input (SKU/Quantity)
  - Hold management with selectable sessions and finalize flow
  - Sales and reports views
  - Setup flows (preview/import/reset/backup/restore)
- Added confirmation prompts for risky actions in Qt flow:
  - Finalize hold
  - Reset DB
  - Restore DB (two-step confirmation)
- Extended i18n keys to support Qt dialogs/messages/placeholders.
- Removed dead code in Qt UI layer (`PlaceholderPage`).
- Added operational docs:
  - `docs/UI_QUICKSTART.md`
  - `docs/RELEASE_PYINSTALLER.md`

## Next Phase
1. PySide6 i18n polish
- Move remaining static table header text to translator-managed labels.
- Localize all dialog button text/content consistently.

2. Release QA
- Run end-to-end smoke on both entrypoints (`app.py`, `app_qt.py`).
- Validate setup operations in packaged runtime.

3. Packaging updates
- Add optional PyInstaller target for Qt entrypoint.
- Verify hidden imports/resources needed for PySide6 distribution.

## Risks / Notes
- Runtime without Tk support cannot execute real UI tests.
- `.xlsx` import requires `openpyxl`; fallback CSV path remains available.

## Reference
- Project init requirement and structure: WAREHOUSE_APP_SPEC.md 
