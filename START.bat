@echo off
title Pixel Blade Fishing Bot
python main.pyw
if errorlevel 1 (
    echo.
    echo Error: Could not start the bot. Make sure Python is installed.
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Please run START.bat again after installation.
)
pause
