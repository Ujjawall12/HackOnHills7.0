@echo off
REM Manhattan Project - Setup Script for Hackathon (Batch version)
echo === Manhattan Project Setup ===
echo Installing dependencies for all components...

REM Media Creator
echo.
echo [1/3] Installing Media Creator dependencies...
cd client\media_creator
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing Media Creator dependencies!
    exit /b 1
)

REM Wallet App
echo.
echo [2/3] Installing Wallet App dependencies...
cd ..\wallet_app
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing Wallet App dependencies!
    exit /b 1
)

REM Sanitization Engine GUI
echo.
echo [3/3] Installing Sanitization Engine GUI dependencies...
cd ..\..\sanitization_engine\gui
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing Sanitization Engine GUI dependencies!
    exit /b 1
)

cd ..\..\..

echo.
echo === Setup Complete! ===
echo All dependencies installed successfully!
echo.
echo To run the applications:
echo   Media Creator: python client\media_creator\main.py
echo   Wallet App: python client\wallet_app\main.py
echo   Sanitization Engine: python sanitization_engine\gui\main.py
pause

