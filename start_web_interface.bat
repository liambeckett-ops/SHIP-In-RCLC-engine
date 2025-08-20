@echo off
echo 🚀 Starting Solvine Web Interface with Jasper Integration
echo.
echo This will start the web server that connects your beautiful UI to the actual Jasper agent!
echo.

cd /d "%~dp0"

echo 📂 Current directory: %CD%
echo.

if not exist "web_api_server.py" (
    echo ❌ Error: web_api_server.py not found in current directory
    echo    Make sure you're running this from the Solvine_Systems directory
    pause
    exit /b 1
)

if not exist "web\solvine_web_ui.html" (
    echo ❌ Error: web\solvine_web_ui.html not found
    echo    The web interface file is missing
    pause
    exit /b 1
)

echo ✅ Files found, starting server...
echo.
echo 🌐 Web Interface will be available at: http://localhost:8080
echo 📖 API Documentation will be at: http://localhost:8080/docs
echo.
echo ⚠️  Important: Use exactly "localhost:8080" (not "localhost:808")
echo    If you see a redirect to solvine_web_ui.html, just go back to localhost:8080
echo.
echo 💡 To stop the server, press Ctrl+C
echo.

python web_api_server.py --port 8080

echo.
echo 🔄 Server stopped.
pause
