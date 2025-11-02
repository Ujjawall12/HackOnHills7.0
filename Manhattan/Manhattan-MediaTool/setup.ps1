# Manhattan Project - Setup Script for Hackathon
# This script installs all dependencies for all components

Write-Host "=== Manhattan Project Setup ===" -ForegroundColor Cyan
Write-Host "Installing dependencies for all components..." -ForegroundColor Yellow

# Media Creator
Write-Host "`n[1/3] Installing Media Creator dependencies..." -ForegroundColor Green
Set-Location client\media_creator
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing Media Creator dependencies!" -ForegroundColor Red
    exit 1
}

# Wallet App
Write-Host "`n[2/3] Installing Wallet App dependencies..." -ForegroundColor Green
Set-Location ..\wallet_app
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing Wallet App dependencies!" -ForegroundColor Red
    exit 1
}

# Sanitization Engine GUI
Write-Host "`n[3/3] Installing Sanitization Engine GUI dependencies..." -ForegroundColor Green
Set-Location ..\..\sanitization_engine\gui
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing Sanitization Engine GUI dependencies!" -ForegroundColor Red
    exit 1
}

Set-Location ..\..\..

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host "All dependencies installed successfully!" -ForegroundColor Green
Write-Host "`nTo run the applications:" -ForegroundColor Yellow
Write-Host "  Media Creator: python client\media_creator\main.py" -ForegroundColor White
Write-Host "  Wallet App: python client\wallet_app\main.py" -ForegroundColor White
Write-Host "  Sanitization Engine: python sanitization_engine\gui\main.py" -ForegroundColor White

