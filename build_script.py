#!/usr/bin/env python3
"""
Automated build script for Pressure Vessel Cost Calculator
Creates executables for Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import platform
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    dependencies = [
        "customtkinter>=5.2.0",
        "pypdf>=3.0.0", 
        "pandas>=1.5.0",
        "openpyxl>=3.1.0",
        "openai>=1.0.0",
        "Pillow>=9.0.0",
        "requests>=2.28.0",
        "pyinstaller>=5.0.0"
    ]
    
    print("📦 Installing dependencies...")
    for dep in dependencies:
        if not run_command([sys.executable, "-m", "pip", "install", dep], f"Installing {dep.split('>=')[0]}"):
            return False
    return True

def create_app_icon():
    """Create a simple app icon if none exists"""
    if not os.path.exists("app.ico") and not os.path.exists("app.png"):
        print("🎨 Creating default app icon...")
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple icon
            img = Image.new('RGB', (256, 256), color='#1f4e79')
            draw = ImageDraw.Draw(img)
            
            # Draw a simple vessel shape
            draw.ellipse([50, 80, 206, 120], fill='white', outline='#366092', width=4)
            draw.rectangle([50, 100, 206, 180], fill='white', outline='#366092', width=4)
            draw.ellipse([50, 160, 206, 200], fill='white', outline='#366092', width=4)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            draw.text((128, 220), "PVC", anchor="mm", fill='white', font=font)
            
            # Save as ICO for Windows and PNG for others
            if platform.system() == "Windows":
                img.save("app.ico", format='ICO')
            else:
                img.save("app.png", format='PNG')
            
            print("✅ Default app icon created")
            return True
        except ImportError:
            print("⚠️ Pillow not available for icon creation, continuing without icon")
            return True
        except Exception as e:
            print(f"⚠️ Could not create icon: {e}")
            return True

def build_executable():
    """Build the executable using PyInstaller"""
    app_name = "PressureVesselCalculator"
    main_script = "pressure_vessel_app.py"
    
    if not os.path.exists(main_script):
        print(f"❌ Main script '{main_script}' not found!")
        return False
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", app_name,
        "--clean",
        "--noconfirm"
    ]
    
    # Add icon if available
    system = platform.system()
    if system == "Windows" and os.path.exists("app.ico"):
        cmd.extend(["--icon", "app.ico"])
    elif system in ["Darwin", "Linux"] and os.path.exists("app.png"):
        cmd.extend(["--icon", "app.png"])
    
    # Add hidden imports for common issues
    hidden_imports = [
        "customtkinter",
        "pypdf",
        "pandas", 
        "openpyxl",
        "openai",
        "PIL",
        "requests"
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    # Add the main script
    cmd.append(main_script)
    
    print("🔨 Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    return run_command(cmd, "Building executable")

def get_executable_path():
    """Get the path to the built executable"""
    system = platform.system()
    app_name = "PressureVesselCalculator"
    
    if system == "Windows":
        return Path("dist") / f"{app_name}.exe"
    elif system == "Darwin":
        return Path("dist") / f"{app_name}.app"
    else:
        return Path("dist") / app_name

def test_executable():
    """Test if the executable can be run"""
    exe_path = get_executable_path()
    
    if not exe_path.exists():
        print(f"❌ Executable not found at {exe_path}")
        return False
    
    print(f"✅ Executable created: {exe_path}")
    print(f"📏 File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    return True

def create_release_package():
    """Create a release package with documentation"""
    print("📦 Creating release package...")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executable
    exe_path = get_executable_path()
    if exe_path.exists():
        if exe_path.is_dir():  # macOS .app bundle
            shutil.copytree(exe_path, release_dir / exe_path.name)
        else:
            shutil.copy2(exe_path, release_dir)
    
    # Create README for end users
    readme_content = f"""# Pressure Vessel Cost Calculator

## Quick Start

1. **Run the application:**
   - Windows: Double-click `PressureVesselCalculator.exe`
   - macOS: Double-click `PressureVesselCalculator.app`
   - Linux: Run `./PressureVesselCalculator` in terminal

2. **Get OpenAI API Key:**
   - Visit: https://platform.openai.com/api-keys
   - Create account and generate API key
   - Enter key in the application

3. **Process a PDF:**
   - Click "Browse" to select your pressure vessel PDF
   - Choose output directory
   - Click "Process PDF & Generate Cost Calculator"
   - Wait for Excel file to be created

## Features

- AI-enhanced cost estimation
- Professional Excel output
- Cross-platform compatibility
- Budget and Full AI modes
- Automatic file management

## System Requirements

- Windows 10+, macOS 10.14+, or Linux with GUI
- Internet connection for AI features
- OpenAI API key for cost estimation

## Cost Estimates

- Budget Mode: ~$0.10 per analysis
- Full Mode: ~$0.25 per analysis

## Support

For technical support or questions, contact your system administrator.

Built on {platform.system()} {platform.release()}
"""
    
    with open(release_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Release package created in '{release_dir}'")
    return True

def main():
    """Main build process"""
    print("🚀 PRESSURE VESSEL CALCULATOR - BUILD SCRIPT")
    print("=" * 50)
    
    # Check system compatibility
    if not check_python_version():
        return False
    
    print(f"🖥️ Building for {platform.system()} {platform.release()}")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Create app icon
    create_app_icon()
    
    # Build executable
    if not build_executable():
        print("❌ Failed to build executable")
        return False
    
    # Test executable
    if not test_executable():
        print("❌ Executable test failed")
        return False
    
    # Create release package
    create_release_package()
    
    print("\n🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("\n📁 Files created:")
    
    exe_path = get_executable_path()
    if exe_path.exists():
        print(f"   • Executable: {exe_path}")
        print(f"   • Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    print(f"   • Release package: release/")
    print(f"   • Documentation: release/README.txt")
    
    print("\n📋 Next steps:")
    print("   1. Test the executable by running it")
    print("   2. Distribute the 'release' folder to end users")
    print("   3. Users only need the executable - no Python installation required!")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)