# Solvine Systems PowerShell Profile
# Add this to your PowerShell profile to automatically navigate to Solvine directory

function Go-Solvine {
    <#
    .SYNOPSIS
    Navigate to Solvine Systems project directory
    .DESCRIPTION
    Quick function to jump to the Solvine Systems directory and show helpful commands
    #>
    
    $SolvinePath = "C:\Users\rebek\OneDrive\Documents\Schoolwork\Programming\Personal Projects\Solvine_Systems"
    
    if (Test-Path $SolvinePath) {
        Set-Location $SolvinePath
        Write-Host "🚀 Solvine Systems Environment Ready!" -ForegroundColor Green
        Write-Host "📁 Current Directory: " -NoNewline
        Write-Host (Get-Location) -ForegroundColor Cyan
        Write-Host ""
        Write-Host "💡 Quick Commands:" -ForegroundColor Yellow
        Write-Host "   python web_api_server.py     - Start web interface"
        Write-Host "   python quick_jasper_test.py  - Test Jasper"
        Write-Host "   python comprehensive_jasper_test.py - Full test"
        Write-Host "   Test-Jasper                  - Run Jasper test (PowerShell function)"
        Write-Host "   Start-SolvineWeb             - Start web server (PowerShell function)"
        Write-Host ""
    } else {
        Write-Host "❌ Solvine Systems directory not found at: $SolvinePath" -ForegroundColor Red
    }
}

function Test-Jasper {
    <#
    .SYNOPSIS
    Quick Jasper test function
    #>
    
    $SolvinePath = "C:\Users\rebek\OneDrive\Documents\Schoolwork\Programming\Personal Projects\Solvine_Systems"
    if (Test-Path $SolvinePath) {
        Set-Location $SolvinePath
        python quick_jasper_test.py
    } else {
        Write-Host "❌ Please navigate to Solvine directory first" -ForegroundColor Red
    }
}

function Start-SolvineWeb {
    <#
    .SYNOPSIS
    Start Solvine web server
    #>
    
    $SolvinePath = "C:\Users\rebek\OneDrive\Documents\Schoolwork\Programming\Personal Projects\Solvine_Systems"
    if (Test-Path $SolvinePath) {
        Set-Location $SolvinePath
        Write-Host "🌐 Starting Solvine Web Server..." -ForegroundColor Green
        python web_api_server.py
    } else {
        Write-Host "❌ Please navigate to Solvine directory first" -ForegroundColor Red
    }
}

# Create aliases for convenience
Set-Alias -Name solvine -Value Go-Solvine
Set-Alias -Name jasper -Value Test-Jasper
Set-Alias -Name webserver -Value Start-SolvineWeb

# Auto-navigate to Solvine on profile load (optional - uncomment if desired)
# Go-Solvine
