@echo off
echo Starting Solvine Web API Server...
echo Current directory: %CD%
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Checking for existing server on port 8080...
netstat -ano | findstr :8080
if not errorlevel 1 (
    echo WARNING: Something is already running on port 8080!
    echo You may need to stop it first.
    pause
)

echo.
echo Starting FastAPI server...
cd /d "%~dp0"
python web_api_server.py --port 8080

pause
