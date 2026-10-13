@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo    Running Pytest Automated Tests
echo ======================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run run_project.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pytest test_app.py -v

echo.
echo ======================================================================
pause
