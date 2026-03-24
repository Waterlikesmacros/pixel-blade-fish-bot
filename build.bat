@echo off
title Pixel Blade Fishing Bot - Build Executable
echo ========================================
echo   Building No-Console Executable
echo ========================================
echo.
echo This will create an .exe file with no console window
echo.
pause
python build_exe.py
echo.
echo ========================================
echo Build process completed!
echo.
if exist dist\pixelBladeFishingBot.exe (
    echo SUCCESS: Executable created at dist\pixelBladeFishingBot.exe
    echo You can now run this file directly with no console!
) else (
    echo ERROR: Build failed. Check error messages above.
)
echo.
pause
