# Solvine API Server PowerShell Launcher
# Quick launcher for the FastAPI/CLI interface

Write-Host "🚀 SOLVINE API SERVER LAUNCHER" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Change to script directory to ensure correct paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Write-Host "📁 Working directory: $PWD" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python not found. Please install Python." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if FastAPI is installed
try {
    python -c "import fastapi" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ FastAPI already installed" -ForegroundColor Green
    } else {
        throw "FastAPI not found"
    }
} catch {
    Write-Host "⚠️  FastAPI not detected. Installing API requirements..." -ForegroundColor Yellow
    
    # Check if requirements file exists
    if (-not (Test-Path "api_requirements.txt")) {
        Write-Host "❌ api_requirements.txt not found in current directory" -ForegroundColor Red
        Write-Host "📁 Current directory: $PWD" -ForegroundColor Yellow
        Write-Host "📋 Available .txt files:" -ForegroundColor Yellow
        Get-ChildItem -Filter "*.txt" | ForEach-Object { Write-Host "   $($_.Name)" }
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r api_requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install requirements" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✅ Dependencies ready" -ForegroundColor Green

# Start the API server
Write-Host ""
Write-Host "🚀 Starting Solvine API Server..." -ForegroundColor Cyan
Write-Host "📖 API Documentation will be available at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "🔧 CLI Access: python solvine_cli.py --interactive" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Magenta
Write-Host ""

# Start the server
python solvine_api_server.py --reload

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Server failed to start" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
