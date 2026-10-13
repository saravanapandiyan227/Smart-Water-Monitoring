@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo    Smart Water Monitoring and Complaint Management System
echo    Local Launcher (AquaWatch)
echo ======================================================================
echo.

cd /d "%~dp0"

:: 1. Detect Python 3.11 or Python 3
set "PY_CMD="
py -3.11 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3.11"
    goto :PYTHON_FOUND
)

py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto :PYTHON_FOUND
)

python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto :PYTHON_FOUND
)

echo [ERROR] Python 3 was not found on your system!
echo Please install Python 3.11 from python.org and add it to PATH.
pause
exit /b 1

:PYTHON_FOUND
echo [INFO] Using Python command: %PY_CMD%

:: 2. Check and create virtual environment if missing
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating Python virtual environment in .venv...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
)

:: 3. Install or verify dependencies
echo [INFO] Checking Python dependencies...
".venv\Scripts\pip.exe" install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Dependency install had warnings, continuing...
) else (
    echo [SUCCESS] Dependencies verified.
)

:: 4. Ensure data folder exists
if not exist "data" mkdir "data"

:: 5. Open browser in background after short delay
echo [INFO] Starting Flask server on http://localhost:5000...
start "" cmd /c "timeout /t 2 >nul & start http://localhost:5000"

:: 6. Run Flask application
echo.
echo ======================================================================
echo  AquaWatch is now running!
echo  Open: http://localhost:5000
echo  Admin Credentials: admin / admin123
echo  Press CTRL + C to stop the server.
echo ======================================================================
echo.

".venv\Scripts\python.exe" app.py

pause
