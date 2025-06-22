#!/usr/bin/env python3
"""
Local build script for testing before GitHub Actions
Ensures your app builds correctly on your current platform
"""
import subprocess
import sys
import platform
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'pyinstaller', 'customtkinter', 'pypdf', 'pandas', 
        'openpyxl', 'openai', 'requests', 'PIL'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n💡 Install missing packages:")
        install_cmd = "pip install " + " ".join(missing).replace('PIL', 'Pillow')
        print(f"   {install_cmd}")
        return False
    
    return True

def build_local():
    """Build for current platform"""
    current_platform = platform.system()
    
    print(f"🔨 Building for {current_platform}...")
    
    # Check dependencies first
    if not check_dependencies():
        print("❌ Please install missing dependencies first")
        return False
    
    # Ensure main file exists
    if not Path("pressure_vessel_app.py").exists():
        print("❌ pressure_vessel_app.py not found!")
        print("Make sure you're in the correct directory")
        return False
    
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
    
    # Platform-specific options
    if current_platform == "Windows":
        cmd.extend(["--windowed", "--icon=app.ico"])
        expected = "dist/PressureVesselCalculator.exe"
    elif current_platform == "Darwin":  # macOS
        cmd.extend(["--windowed", "--icon=app.icns"])
        expected = "dist/PressureVesselCalculator"
    else:  # Linux
        expected = "dist/PressureVesselCalculator"
    
    cmd.append("pressure_vessel_app.py")
    
    print(f"🏗️  Running: {' '.join(cmd)}")
    
    # Run build
    try:
        result = subprocess.run(cmd, check=True)
        
        if Path(expected).exists():
            size = Path(expected).stat().st_size / (1024 * 1024)
            print(f"\n✅ Build successful!")
            print(f"📁 Executable: {expected}")
            print(f"📏 Size: {size:.1f} MB")
            
            # Test if executable runs
            print("\n🧪 Testing executable...")
            test_result = subprocess.run([str(Path(expected)), "--help"], 
                                       capture_output=True, text=True, timeout=10)
            if test_result.returncode == 0 or "usage" in test_result.stdout.lower():
                print("✅ Executable test passed")
            else:
                print("⚠️  Executable created but may have issues")
            
            return True
        else:
            print(f"❌ Build completed but executable not found: {expected}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Executable test timed out")
        return True  # Build succeeded, just testing failed

def main():
    """Main function"""
    print("🚀 Local Build Script - Pressure Vessel Calculator")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()
    
    success = build_local()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Local build completed successfully!")
        print("\n💡 Next steps:")
        print("1. Test the executable manually")
        print("2. If it works, push to GitHub for cross-platform builds")
        print("3. GitHub Actions will build for Windows, macOS, and Linux")
    else:
        print("❌ Local build failed")
        print("\n💡 Troubleshooting:")
        print("1. Check that all dependencies are installed")
        print("2. Ensure pressure_vessel_app.py exists")
        print("3. Try running without --windowed flag")
        print("4. Check PyInstaller documentation")

if __name__ == "__main__":
    main()