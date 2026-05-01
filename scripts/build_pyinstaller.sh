#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

uv run --with '.[build]' pyinstaller --clean --noconfirm packaging/py-simple-inventory.spec

echo "Build complete. Output: $ROOT_DIR/dist/PySimpleInventory"
