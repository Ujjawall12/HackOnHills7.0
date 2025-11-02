# Manhattan Project - Quick Run Script
# Easily launch any component of the project

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("media", "wallet", "engine", "demo")]
    [string]$Component
)

$ErrorActionPreference = "Stop"

switch ($Component) {
    "media" {
        Write-Host "Launching Media Creator..." -ForegroundColor Cyan
        Set-Location client\media_creator
        python main.py
    }
    "wallet" {
        Write-Host "Launching Wallet App..." -ForegroundColor Cyan
        Set-Location client\wallet_app
        python main.py
    }
    "engine" {
        Write-Host "Launching Sanitization Engine..." -ForegroundColor Cyan
        Set-Location sanitization_engine\gui
        python main.py
    }
    "demo" {
        Write-Host "Launching Secure File Deletion Demo..." -ForegroundColor Cyan
        python demo_secure_delete_gui.py
    }
}

