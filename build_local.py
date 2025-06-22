#!/usr/bin/env python3
"""
Local build script for testing before GitHub Actions
"""
import subprocess
import sys
import platform
from pathlib import Path

def build_local():
    """Build for current platform"""
    current_platform = platform.system()
    
    print(f"🔨 Building for {current_platform}...")
    
    # Install dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Build command
    cmd = [
        "pyinstaller",
        "--clean",
        "--onefile",
        "--name", "PressureVesselCalculator",
        "--hidden-import", "customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "PIL._tkinter_finder"
    ]
    
    if current_platform == "Windows":
        cmd.extend(["--windowed", "--icon=app.ico"])
        expected = "dist/PressureVesselCalculator.exe"
    elif current_platform == "Darwin":  # macOS
        cmd.extend(["--windowed", "--icon=app.icns"])
        expected = "dist/PressureVesselCalculator"
    else:  # Linux
        expected = "dist/PressureVesselCalculator"
    
    cmd.append("pressure_vessel_app.py")
    
    # Run build
    result = subprocess.run(cmd)
    
    if result.returncode == 0 and Path(expected).exists():
        size = Path(expected).stat().st_size / (1024 * 1024)
        print(f"✅ Build successful: {expected} ({size:.1f} MB)")
    else:
        print("❌ Build failed")

if __name__ == "__main__":
    build_local()