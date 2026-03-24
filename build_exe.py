#!/usr/bin/env python3
"""
Build Pixel Blade Fishing Bot as executable with no console
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_executable():
    """Build the executable with no console"""
    print("Building executable with no console...")
    
    # Build command - fixed icon handling
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--windowed", 
        "--name=PixelBladeFishingBot",
        "main.pyw"
    ]
    
    # Add icon if it exists
    if os.path.exists("icon.ico"):
        cmd.insert(-1, "--icon=icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("Build successful!")
        print("Executable created: dist/PixelBladeFishingBot.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def main():
    """Main build function"""
    print("=== Pixel Blade Fishing Bot Builder ===")
    print()
    
    # Step 1: Install PyInstaller
    if not install_pyinstaller():
        print("Failed to install PyInstaller")
        return
    
    print()
    
    # Step 2: Build executable
    if build_executable():
        print()
        print("=== Build Complete ===")
        print("You can now run dist/PixelBladeFishingBot.exe")
        print("No console window will appear!")
    else:
        print("=== Build Failed ===")
        print("Check the error messages above")

if __name__ == "__main__":
    main()
