@echo off
setlocal
cd /d %~dp0\..
uv run --with .[build] pyinstaller --clean --noconfirm packaging/py-simple-inventory.spec
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
echo Build complete. Output: %CD%\dist\PySimpleInventory
