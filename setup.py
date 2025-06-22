#!/usr/bin/env python3
# ===============================================
# AUTOMATED CROSS-PLATFORM BUILD SETUP
# Run this script to set up everything automatically
# ===============================================

import os
import sys
import subprocess
from pathlib import Path
import json

def create_github_workflow():
    """Create GitHub Actions workflow file"""
    workflow_content = '''name: 🚀 Build Pressure Vessel Calculator

on:
  push:
    branches: [ main, master ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: windows-latest
            platform: windows
            output_name: PressureVesselCalculator.exe
          - os: macos-latest
            platform: macos
            output_name: PressureVesselCalculator
          - os: ubuntu-latest
            platform: linux
            output_name: PressureVesselCalculator

    steps:
    - name: 📥 Checkout Code
      uses: actions/checkout@v4
    
    - name: 🐍 Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: 📦 Install Dependencies (Ubuntu)
      if: matrix.platform == 'linux'
      run: |
        sudo apt-get update
        sudo apt-get install -y python3-tk python3-dev

    - name: 📦 Install Python Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pyinstaller>=5.0
        pip install customtkinter>=5.2.0
        pip install pypdf>=3.0.0
        pip install pandas>=1.5.0
        pip install openpyxl>=3.0.0
        pip install openai>=1.0.0
        pip install requests>=2.28.0
        pip install Pillow>=9.0.0

    - name: 🏗️ Build Application (Windows)
      if: matrix.platform == 'windows'
      run: |
        pyinstaller --clean --onefile --windowed --name "PressureVesselCalculator" --icon=app.ico --hidden-import customtkinter --hidden-import tkinter --hidden-import tkinter.filedialog --hidden-import tkinter.messagebox --hidden-import PIL._tkinter_finder pressure_vessel_app.py

    - name: 🏗️ Build Application (macOS)
      if: matrix.platform == 'macos'
      run: |
        pyinstaller --clean --onefile --windowed --name "PressureVesselCalculator" --icon=app.icns --hidden-import customtkinter --hidden-import tkinter --hidden-import tkinter.filedialog --hidden-import tkinter.messagebox --hidden-import PIL._tkinter_finder pressure_vessel_app.py

    - name: 🏗️ Build Application (Linux)
      if: matrix.platform == 'linux'
      run: |
        pyinstaller --clean --onefile --name "PressureVesselCalculator" --hidden-import customtkinter --hidden-import tkinter --hidden-import tkinter.filedialog --hidden-import tkinter.messagebox --hidden-import PIL._tkinter_finder pressure_vessel_app.py

    - name: 📤 Upload Artifacts
      uses: actions/upload-artifact@v4
      with:
        name: PressureVesselCalculator-${{ matrix.platform }}
        path: |
          dist/${{ matrix.output_name }}
        retention-days: 30

  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - name: 📥 Download All Artifacts
        uses: actions/download-artifact@v4
        with:
            path: artifacts

    - name: 📦 Prepare Release Assets
    run: |
        mkdir release-assets
        cp artifacts/PressureVesselCalculator-windows/PressureVesselCalculator.exe release-assets/
        cp artifacts/PressureVesselCalculator-macos/PressureVesselCalculator release-assets/
        cp artifacts/PressureVesselCalculator-linux/PressureVesselCalculator release-assets/
        chmod +x release-assets/PressureVesselCalculator-macOS
        chmod +x release-assets/PressureVesselCalculator-Linux

    - name: 🚀 Create GitHub Release
      uses: softprops/action-gh-release@v2
      with:
        files: release-assets/*
        draft: false
        prerelease: false
        body: |
          ## 🎉 Pressure Vessel Calculator Release
          
          **Cross-platform builds available:**
          
          ### 🪟 Windows
          - `PressureVesselCalculator-Windows.exe` - Ready to run
          
          ### 🍎 macOS
          - `PressureVesselCalculator-macOS` - Make executable and run
          
          ### 🐧 Linux
          - `PressureVesselCalculator-Linux` - Make executable and run
          
          Built automatically with GitHub Actions ✨
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
    
    # Create .github/workflows directory
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    # Write workflow file
    workflow_file = workflow_dir / 'build.yml'
    with open(workflow_file, 'w') as f:
        f.write(workflow_content.strip())
    
    print(f"✅ Created GitHub workflow: {workflow_file}")

def create_requirements_txt():
    """Create requirements.txt file"""
    requirements = '''customtkinter>=5.2.0
pypdf>=3.0.0
pandas>=1.5.0
openpyxl>=3.0.0
openai>=1.0.0
requests>=2.28.0
Pillow>=9.0.0
pyinstaller>=5.0.0
pathlib2>=2.3.0
'''
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements.strip())
    
    print("✅ Created requirements.txt")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Virtual environments
venv/
env/
ENV/
build_env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon?

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# Settings
.pressure_vessel_app_settings.json

# Logs
*.log

# Test files
test_*.py
temp_*
'''
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    print("✅ Created .gitignore")

def create_readme():
    """Create README.md file"""
    readme_content = '''# 🚀 AI-Enhanced Pressure Vessel Cost Calculator

Modern, intelligent cost estimation for pressure vessel projects with AI integration.

## ✨ Features

- 📄 **PDF Analysis**: Automatically extract vessel specifications from PDF documents
- 🤖 **AI Integration**: OpenAI-powered cost estimation and analysis
- 📊 **Excel Reports**: Generate professional cost calculation spreadsheets
- 📧 **Email Integration**: Send quotes directly to customers
- 🎨 **Modern UI**: Beautiful, intuitive interface with dark/light themes
- 🔄 **Cross-Platform**: Available for Windows, macOS, and Linux

## 📥 Download

### Latest Release
- 🪟 **Windows**: [Download .exe](../../releases/latest)
- 🍎 **macOS**: [Download executable](../../releases/latest)  
- 🐧 **Linux**: [Download executable](../../releases/latest)

### Requirements
- No additional dependencies needed (everything bundled)
- Internet connection for AI features
- OpenAI API key for enhanced analysis

## 🚀 Quick Start

1. **Download** the appropriate file for your platform
2. **Run** the executable
3. **Configure** your OpenAI API key (optional but recommended)
4. **Upload** a pressure vessel PDF
5. **Generate** cost calculations
6. **Export** to Excel or email to customers

## 🔧 Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/yourusername/pressure-vessel-calculator.git
cd pressure-vessel-calculator

# Install dependencies
pip install -r requirements.txt

# Run application
python pressure_vessel_app.py

# Build executable
pyinstaller --onefile --windowed pressure_vessel_app.py
```

### Cross-Platform Building

This project uses GitHub Actions for automatic cross-platform builds:

1. Push changes to GitHub
2. Builds automatically create executables for Windows, macOS, and Linux
3. Download artifacts from the Actions tab
4. Create releases by tagging: `git tag v1.0.0 && git push origin v1.0.0`

## 📋 Usage

### Step 1: Upload PDF
- Select your pressure vessel specification PDF
- The app will automatically extract key information

### Step 2: Configure AI (Optional)
- Add your OpenAI API key for enhanced analysis
- Choose budget mode for cost-effective processing

### Step 3: Generate Report
- Click "Generate Cost Calculator"
- Review extracted information and AI analysis
- Export to Excel format

### Step 4: Send Quote
- Enter customer email address
- Send professional quote directly

## 🔑 API Key Setup

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and paste into the app
4. Test connection

**Cost**: ~$0.10-0.25 per analysis depending on mode

## 🛠️ Technical Details

- **Framework**: Python with CustomTkinter for modern UI
- **PDF Processing**: PyPDF for text extraction
- **AI Integration**: OpenAI API for intelligent analysis
- **Excel Export**: OpenPyXL for professional reports
- **Email**: Webhook integration for quote delivery

## 📸 Screenshots

[Add screenshots of the application here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Add your license here]

## 🆘 Support

- 📧 Email: support@yourcompany.com
- 🐛 Issues: [GitHub Issues](../../issues)
- 📖 Documentation: [Wiki](../../wiki)

---

Built with ❤️ using Python and modern web technologies
'''
    
    with open('README.md', 'w') as f:
        f.write(readme_content.strip())
    
    print("✅ Created README.md")

def create_placeholder_icons():
    """Create placeholder icon files"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        def create_icon(size, filename):
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple gear icon
            center = size // 2
            radius = size // 3
            
            # Outer circle
            draw.ellipse([center-radius, center-radius, center+radius, center+radius], 
                        fill=(0, 123, 191, 255), outline=(0, 100, 150, 255), width=2)
            
            # Inner circle
            inner_radius = radius // 3
            draw.ellipse([center-inner_radius, center-inner_radius, center+inner_radius, center+inner_radius], 
                        fill=(255, 255, 255, 255))
            
            # Gear teeth (simplified)
            for i in range(8):
                angle = i * 45
                import math
                x1 = center + radius * math.cos(math.radians(angle))
                y1 = center + radius * math.sin(math.radians(angle))
                x2 = center + (radius + 10) * math.cos(math.radians(angle))
                y2 = center + (radius + 10) * math.sin(math.radians(angle))
                draw.line([x1, y1, x2, y2], fill=(0, 123, 191, 255), width=3)
            
            img.save(filename)
            return filename
        
        # Create PNG first
        png_file = create_icon(256, 'icon.png')
        print(f"✅ Created base icon: {png_file}")
        
        # Create ICO for Windows
        img = Image.open('icon.png')
        img.save('app.ico', format='ICO', sizes=[(256, 256)])
        print("✅ Created Windows icon: app.ico")
        
        # For macOS, we'll create a simple PNG and give instructions
        larger_icon = create_icon(1024, 'icon_large.png')
        print("✅ Created large icon for macOS conversion")
        print("💡 To create app.icns, run: iconutil -c icns icon_large.png")
        
        # Try to create icns if iconutil is available (macOS only)
        try:
            subprocess.run(['iconutil', '-c', 'icns', 'icon_large.png', '-o', 'app.icns'], 
                         check=True, capture_output=True)
            print("✅ Created macOS icon: app.icns")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Manual creation for macOS
            img_large = Image.open('icon_large.png')
            img_large.save('app.icns', format='ICNS')
            print("✅ Created basic macOS icon: app.icns")
        
    except ImportError:
        print("⚠️  Pillow not installed - creating placeholder text files")
        
        # Create placeholder files
        with open('app.ico', 'w') as f:
            f.write("# Placeholder - Replace with actual .ico file\n")
        with open('app.icns', 'w') as f:
            f.write("# Placeholder - Replace with actual .icns file\n")
        
        print("💡 Install Pillow to auto-generate icons: pip install Pillow")
        print("💡 Or create icons manually:")
        print("   - Windows: 256x256 PNG → .ico file")
        print("   - macOS: 1024x1024 PNG → .icns file")

def create_local_build_script():
    """Create local build script for testing"""
    build_script = '''#!/usr/bin/env python3
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
'''
    
    with open('build_local.py', 'w') as f:
        f.write(build_script.strip())
    
    print("✅ Created local build script: build_local.py")

def check_git_repo():
    """Check if we're in a git repository"""
    try:
        subprocess.run(['git', 'status'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo():
    """Initialize git repository"""
    if not check_git_repo():
        print("🔧 Initializing Git repository...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'branch', '-M', 'main'])
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Cross-Platform Build Environment")
    print("=" * 60)
    
    # Check if main app file exists
    if not Path("pressure_vessel_app.py").exists():
        print("❌ pressure_vessel_app.py not found!")
        print("Make sure you're in the correct directory with your app file.")
        sys.exit(1)
    
    print("📁 Current directory:", Path.cwd())
    print()
    
    # Create all necessary files
    create_requirements_txt()
    create_gitignore()
    create_readme()
    create_github_workflow()
    create_placeholder_icons()
    create_local_build_script()
    
    # Initialize git repo
    init_git_repo()
    
    print()
    print("=" * 60)
    print("🎉 Setup Complete!")
    print()
    print("📋 Next Steps:")
    print("1. 🔧 Test local build:")
    print("   python build_local.py")
    print()
    print("2. 🔗 Create GitHub repository:")
    print("   - Go to github.com and create new repository")
    print("   - Copy the repository URL")
    print()
    print("3. 📤 Push to GitHub:")
    print("   git add .")
    print('   git commit -m "Initial commit with cross-platform build"')
    print("   git remote add origin YOUR_GITHUB_REPO_URL")
    print("   git push -u origin main")
    print()
    print("4. 🏗️ Automatic builds will start!")
    print("   - Go to Actions tab in your GitHub repo")
    print("   - Download artifacts for all platforms")
    print()
    print("5. 🏷️ Create releases:")
    print("   git tag v1.0.0")
    print("   git push origin v1.0.0")
    print()
    print("🎯 You'll get:")
    print("   ✅ Windows: .exe file")
    print("   ✅ macOS: executable")  
    print("   ✅ Linux: executable")
    print()
    print("⏱️  Build time: ~10-15 minutes")
    print("💰 Cost: Free (GitHub Actions)")

if __name__ == "__main__":
    main()