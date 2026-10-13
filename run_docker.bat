@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo    Smart Water Monitoring - Docker Build and Run
echo ======================================================================
echo.

:: Verify Docker CLI is accessible
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH!
    echo Please install Docker Desktop and start the Docker daemon.
    pause
    exit /b 1
)

:: 1. Build image
echo [1/4] Building Docker image 'water-monitoring-ci'...
docker build -t water-monitoring-ci .
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker build failed! Ensure Docker Desktop is running.
    pause
    exit /b 1
)

:: 2. Create Docker volume
echo [2/4] Ensuring Docker volume 'water_monitoring_data' exists...
docker volume create water_monitoring_data

:: 3. Stop existing container if running
echo [3/4] Cleaning up any old container instance...
docker stop water-monitoring-ansible >nul 2>&1
docker rm water-monitoring-ansible >nul 2>&1

:: 4. Run container
echo [4/4] Starting container 'water-monitoring-ansible' on port 5002...
docker run -d ^
  --name water-monitoring-ansible ^
  -p 5002:5000 ^
  -v water_monitoring_data:/app/data ^
  --restart unless-stopped ^
  water-monitoring-ci

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo  [SUCCESS] Container is running!
    echo  Access AquaWatch at: http://localhost:5002
    echo  Admin Credentials: admin / admin123
    echo ======================================================================
    start http://localhost:5002
) else (
    echo [ERROR] Failed to start Docker container.
)

pause
