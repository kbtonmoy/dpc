#!/usr/bin/env python3
"""
Simple launcher for Pressure Vessel Cost Calculator
Handles dependency installation and app startup
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'customtkinter',
        'pypdf', 
        'pandas',
        'openpyxl',
        'openai',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_packages(packages):
    """Install missing packages"""
    print("📦 Installing required packages...")
    
    package_map = {
        'PIL': 'Pillow',
        'customtkinter': 'customtkinter',
        'pypdf': 'pypdf',
        'pandas': 'pandas', 
        'openpyxl': 'openpyxl',
        'openai': 'openai'
    }
    
    for package in packages:
        pip_name = package_map.get(package, package)
        print(f"Installing {pip_name}...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", pip_name
            ], check=True, capture_output=True)
            print(f"✅ {pip_name} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {pip_name}: {e}")
            return False
    
    return True

def launch_app():
    """Launch the main application"""
    app_file = "pressure_vessel_app.py"
    
    if not os.path.exists(app_file):
        print(f"❌ Application file '{app_file}' not found!")
        print("Make sure all files are in the same directory.")
        return False
    
    print("🚀 Launching Pressure Vessel Cost Calculator...")
    
    try:
        # Import and run the app
        sys.path.insert(0, str(Path(__file__).parent))
        from pressure_vessel_app import main
        main()
        return True
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        return False

def main():
    """Main launcher function"""
    print("🏭 PRESSURE VESSEL COST CALCULATOR LAUNCHER")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. Current: {sys.version_info.major}.{sys.version_info.minor}")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"📋 Missing packages: {', '.join(missing)}")
        response = input("Install missing packages? (y/n): ").lower()
        
        if response == 'y':
            if not install_packages(missing):
                print("❌ Package installation failed")
                input("Press Enter to exit...")
                return
        else:
            print("❌ Cannot run without required packages")
            input("Press Enter to exit...")
            return
    else:
        print("✅ All required packages are installed")
    
    # Launch the application
    if not launch_app():
        input("Press Enter to exit...")
        return
    
    print("👋 Application closed")

if __name__ == "__main__":
    main()