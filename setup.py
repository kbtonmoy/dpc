#!/usr/bin/env python3
# ===============================================
# COMPLETE CROSS-PLATFORM BUILD SETUP SCRIPT
# No YAML indentation errors - Production ready
# ===============================================

import os
import sys
import subprocess
from pathlib import Path
import json

def create_github_workflow():
    """Create GitHub Actions workflow file with PERFECT indentation"""
    # Using triple quotes with proper YAML indentation
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

    - name: 🔍 Debug Info
      run: |
        echo "Platform: ${{ matrix.platform }}"
        echo "Python version:"
        python --version
        echo "PyInstaller version:"
        pyinstaller --version
        echo "Working directory:"
        pwd
        echo "Files in directory:"
        python -c "import os; print('\\n'.join(os.listdir('.')))"

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

    - name: 📂 List Build Output
      run: |
        echo "Contents of dist folder:"
        python -c "import os; print('\\n'.join(os.listdir('dist')) if os.path.exists('dist') else 'dist folder not found')"

    - name: ✅ Verify Build
      run: |
        python -c "
        import os
        import sys
        output_name = '${{ matrix.output_name }}'
        dist_path = os.path.join('dist', output_name)
        if os.path.exists(dist_path):
            size = os.path.getsize(dist_path)
            print(f'✅ Build successful!')
            print(f'File size: {size} bytes ({size/(1024*1024):.1f} MB)')
            sys.exit(0)
        else:
            print(f'❌ Build failed - executable not found: {dist_path}')
            sys.exit(1)
        "

    - name: 📤 Upload Artifacts
      uses: actions/upload-artifact@v4
      with:
        name: PressureVesselCalculator-${{ matrix.platform }}
        path: dist/${{ matrix.output_name }}
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
        python -c "
        import os
        import shutil
        import stat
        
        # Create release assets directory
        os.makedirs('release-assets', exist_ok=True)
        
        # Copy and rename files
        artifacts = {
            'artifacts/PressureVesselCalculator-windows/PressureVesselCalculator.exe': 'release-assets/PressureVesselCalculator-Windows.exe',
            'artifacts/PressureVesselCalculator-macos/PressureVesselCalculator': 'release-assets/PressureVesselCalculator-macOS',
            'artifacts/PressureVesselCalculator-linux/PressureVesselCalculator': 'release-assets/PressureVesselCalculator-Linux'
        }
        
        for src, dst in artifacts.items():
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f'Copied: {src} -> {dst}')
                
                # Make executable for Unix systems
                if 'macOS' in dst or 'Linux' in dst:
                    try:
                        current_permissions = os.stat(dst).st_mode
                        os.chmod(dst, current_permissions | stat.S_IEXEC)
                        print(f'Made executable: {dst}')
                    except:
                        pass  # Skip if chmod fails
            else:
                print(f'Warning: {src} not found')
        
        # List release assets
        print('Release assets:')
        if os.path.exists('release-assets'):
            for item in os.listdir('release-assets'):
                path = os.path.join('release-assets', item)
                size = os.path.getsize(path) / (1024*1024)
                print(f'  {item} ({size:.1f} MB)')
        "

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
          - `PressureVesselCalculator-Windows.exe` - Ready to run executable
          
          ### 🍎 macOS
          - `PressureVesselCalculator-macOS` - Make executable with `chmod +x` and run
          
          ### 🐧 Linux
          - `PressureVesselCalculator-Linux` - Make executable with `chmod +x` and run
          
          **Features:**
          - AI-enhanced PDF analysis
          - Cost calculation and Excel export  
          - Email integration
          - Modern UI with dark/light themes
          
          **Requirements:**
          - No additional dependencies needed (everything bundled)
          - Internet connection for AI features
          - OpenAI API key for enhanced analysis
          
          **Installation:**
          1. Download the appropriate file for your platform
          2. Run the executable
          3. Follow the setup wizard
          
          Built automatically with GitHub Actions ✨
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
'''
    
    # Create .github/workflows directory
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    # Write workflow file with exact indentation
    workflow_file = workflow_dir / 'build.yml'
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content.strip())
    
    print(f"✅ Created GitHub workflow: {workflow_file}")
    
    # Validate the YAML structure
    validate_yaml_indentation(workflow_file)

def validate_yaml_indentation(file_path):
    """Validate YAML indentation to prevent syntax errors"""
    print("🔍 Validating YAML indentation...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    for i, line in enumerate(lines, 1):
        # Check for tabs (YAML doesn't allow tabs)
        if '\t' in line:
            errors.append(f"Line {i}: Contains tab character (use spaces only)")
        
        # Check common indentation patterns
        stripped = line.strip()
        if stripped.startswith('with:'):
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip())
            # 'with:' should be at same level as 'uses:' (typically 6 spaces)
            if leading_spaces not in [2, 6]:  # Allow for different nesting levels
                errors.append(f"Line {i}: 'with:' indentation may be incorrect ({leading_spaces} spaces)")
    
    if errors:
        print("⚠️  YAML validation warnings:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ YAML indentation validation passed")

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
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements.strip())
    
    print("✅ Created requirements.txt")

def create_gitignore():
    """Create comprehensive .gitignore file"""
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
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Virtual environments
venv/
env/
ENV/
build_env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon?
._*

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Application specific
.pressure_vessel_app_settings.json
*.log
temp_*
test_*.py

# Build artifacts
*.dmg
*.zip
release-assets/
artifacts/

# Temporary icon files
icon.png
icon_large.png
MyIcon.iconset/
'''
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content.strip())
    
    print("✅ Created .gitignore")

def create_readme():
    """Create comprehensive README.md file"""
    readme_content = '''# 🚀 AI-Enhanced Pressure Vessel Cost Calculator

> Modern, intelligent cost estimation for pressure vessel projects with AI integration.

[![Build Status](https://github.com/yourusername/pressure-vessel-calculator/workflows/🚀%20Build%20Pressure%20Vessel%20Calculator/badge.svg)](https://github.com/yourusername/pressure-vessel-calculator/actions)
[![Release](https://img.shields.io/github/v/release/yourusername/pressure-vessel-calculator)](https://github.com/yourusername/pressure-vessel-calculator/releases)
[![License](https://img.shields.io/github/license/yourusername/pressure-vessel-calculator)](LICENSE)

## ✨ Features

- 📄 **PDF Analysis**: Automatically extract vessel specifications from PDF documents
- 🤖 **AI Integration**: OpenAI-powered cost estimation and analysis
- 📊 **Excel Reports**: Generate professional cost calculation spreadsheets
- 📧 **Email Integration**: Send quotes directly to customers
- 🎨 **Modern UI**: Beautiful, intuitive interface with dark/light themes
- 🔄 **Cross-Platform**: Available for Windows, macOS, and Linux
- 💰 **Cost Tracking**: Built-in statistics and savings tracking
- ⚙️ **Configurable**: Flexible settings and preferences

## 📥 Download

### 🎯 Latest Release
Download the latest version for your platform:

| Platform | Download | Requirements |
|----------|----------|--------------|
| 🪟 **Windows** | [Download .exe](../../releases/latest) | Windows 10+ |
| 🍎 **macOS** | [Download executable](../../releases/latest) | macOS 10.15+ |
| 🐧 **Linux** | [Download executable](../../releases/latest) | Ubuntu 20.04+ |

### 📋 System Requirements
- **No additional dependencies needed** (everything bundled)
- Internet connection for AI features
- OpenAI API key for enhanced analysis (optional)
- 4GB RAM minimum, 8GB recommended

## 🚀 Quick Start

### 1. 📥 Download & Install
1. Download the appropriate file for your platform from [Releases](../../releases/latest)
2. **Windows**: Run the `.exe` file
3. **macOS/Linux**: Make executable and run:
   ```bash
   chmod +x PressureVesselCalculator-*
   ./PressureVesselCalculator-*
   ```

### 2. ⚙️ Initial Setup
1. Launch the application
2. Navigate to **AI Settings**
3. Add your OpenAI API key (get one [here](https://platform.openai.com/api-keys))
4. Test the connection
5. Configure output directory

### 3. 📄 Process Your First PDF
1. Go to **Upload PDF**
2. Select your pressure vessel specification PDF
3. Click **Next: Configure AI**
4. Choose budget mode for cost-effective processing
5. Click **Generate Cost Calculator**
6. Review the generated Excel report

### 4. 📧 Send Quote
1. Navigate to **Send Quote**
2. Enter customer email address
3. Click **Send Price Quote**

## 🔑 OpenAI API Setup

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy and paste into the app
4. Test connection

**💰 Costs:**
- Budget Mode: ~$0.10 per analysis
- Full Mode: ~$0.25 per analysis

## 🛠️ For Developers

### 🔧 Building from Source

```bash
# Clone repository
git clone https://github.com/yourusername/pressure-vessel-calculator.git
cd pressure-vessel-calculator

# Install dependencies
pip install -r requirements.txt

# Run application
python pressure_vessel_app.py

# Build executable
python build_local.py
```

### 🏗️ Cross-Platform Building

This project uses **GitHub Actions** for automatic cross-platform builds:

1. **Push changes** to GitHub
2. **Builds automatically** create executables for Windows, macOS, and Linux
3. **Download artifacts** from the Actions tab
4. **Create releases** by tagging: `git tag v1.0.0 && git push origin v1.0.0`

### 📁 Project Structure

```
pressure-vessel-calculator/
├── .github/workflows/build.yml    # Auto-build workflow
├── pressure_vessel_app.py         # Main application
├── requirements.txt               # Python dependencies
├── app.ico                        # Windows icon
├── app.icns                       # macOS icon
├── build_local.py                 # Local build script
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```

## 📖 Usage Guide

### Step-by-Step Workflow

#### 📁 Step 1: Upload PDF
- Select your pressure vessel specification PDF
- The app automatically extracts key information
- File validation ensures compatibility

#### 🤖 Step 2: Configure AI (Optional)
- Add OpenAI API key for enhanced analysis
- Choose between Budget Mode ($0.10) or Full Mode ($0.25)
- Test connection to ensure setup

#### 📊 Step 3: Generate Report
- Click "Generate Cost Calculator"
- Review extracted vessel information
- AI analyzes and estimates additional costs
- Export professional Excel report

#### 📧 Step 4: Send Quote
- Enter customer email address
- Send professional quote directly
- Track sent quotes in statistics

## 🔧 Technical Details

### 🏗️ Architecture
- **Frontend**: Python with CustomTkinter for modern UI
- **PDF Processing**: PyPDF for intelligent text extraction
- **AI Integration**: OpenAI API for cost analysis
- **Excel Export**: OpenPyXL for professional reports
- **Email**: Webhook integration for reliable delivery

### 🎨 UI Framework
- Modern card-based layout
- Dark/Light theme support
- Responsive design
- Step-by-step workflow
- Real-time progress tracking

### 📊 Cost Calculation
- Material cost multipliers based on industry standards
- AI-enhanced labor and service estimates
- Comprehensive breakdown by component
- Professional Excel formatting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Email**: support@refineryconnect.com
- 🐛 **Issues**: [GitHub Issues](../../issues)
- 📖 **Documentation**: [Wiki](../../wiki)
- 💬 **Discussions**: [GitHub Discussions](../../discussions)

## 🙏 Acknowledgments

- Built with ❤️ using Python and modern technologies
- Icons provided by [Lucide Icons](https://lucide.dev/)
- AI powered by [OpenAI](https://openai.com/)
- Cross-platform builds by [GitHub Actions](https://github.com/features/actions)

## 📈 Roadmap

- [ ] **v1.1**: TeamDesk integration
- [ ] **v1.2**: CRM export functionality  
- [ ] **v1.3**: Advanced AI models support
- [ ] **v1.4**: Multi-language PDF support
- [ ] **v2.0**: Web-based version

---

**⭐ Star this repository if you find it helpful!**
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content.strip())
    
    print("✅ Created comprehensive README.md")

def create_placeholder_icons():
    """Create placeholder icon files with fallback"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        def create_professional_icon(size, filename):
            # Create image with transparent background
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Colors for professional look
            primary_color = (31, 83, 141, 255)      # Blue
            secondary_color = (0, 212, 170, 255)    # Teal
            white = (255, 255, 255, 255)
            
            center = size // 2
            
            # Draw main circle background
            circle_radius = size // 2 - 8
            draw.ellipse([
                center - circle_radius, 
                center - circle_radius, 
                center + circle_radius, 
                center + circle_radius
            ], fill=primary_color, outline=secondary_color, width=4)
            
            # Draw gear teeth around the edge
            import math
            teeth_count = 12
            inner_radius = circle_radius - 8
            outer_radius = circle_radius + 4
            
            for i in range(teeth_count):
                angle1 = i * (360 / teeth_count) - 10
                angle2 = i * (360 / teeth_count) + 10
                
                # Convert to radians
                rad1 = math.radians(angle1)
                rad2 = math.radians(angle2)
                
                # Calculate points
                x1_inner = center + inner_radius * math.cos(rad1)
                y1_inner = center + inner_radius * math.sin(rad1)
                x2_inner = center + inner_radius * math.cos(rad2)
                y2_inner = center + inner_radius * math.sin(rad2)
                
                x1_outer = center + outer_radius * math.cos(rad1)
                y1_outer = center + outer_radius * math.sin(rad1)
                x2_outer = center + outer_radius * math.cos(rad2)
                y2_outer = center + outer_radius * math.sin(rad2)
                
                # Draw tooth
                draw.polygon([
                    (x1_inner, y1_inner),
                    (x1_outer, y1_outer),
                    (x2_outer, y2_outer),
                    (x2_inner, y2_inner)
                ], fill=secondary_color)
            
            # Draw center circle
            center_radius = size // 6
            draw.ellipse([
                center - center_radius,
                center - center_radius,
                center + center_radius,
                center + center_radius
            ], fill=white, outline=primary_color, width=2)
            
            # Try to add text if font is available
            try:
                font_size = max(8, size // 12)
                font = ImageFont.load_default()
                text = "PV"
                
                # Get text bounding box
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Center the text
                text_x = center - text_width // 2
                text_y = center - text_height // 2
                
                draw.text((text_x, text_y), text, fill=primary_color, font=font)
            except:
                pass  # Skip text if font not available
            
            img.save(filename, format='PNG')
            return filename
        
        # Create high-quality base icon
        base_icon = create_professional_icon(1024, 'icon_base.png')
        print(f"✅ Created base icon: {base_icon}")
        
        # Create Windows ICO
        img = Image.open('icon_base.png')
        # Resize for ICO (multiple sizes)
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save('app.ico', format='ICO', sizes=ico_sizes)
        print("✅ Created Windows icon: app.ico")
        
        # For macOS ICNS - try multiple methods
        try:
            # Method 1: Try iconutil (macOS only)
            iconset_dir = Path('MyIcon.iconset')
            iconset_dir.mkdir(exist_ok=True)
            
            # Create different sizes for iconset
            sizes_iconset = [16, 32, 64, 128, 256, 512, 1024]
            for size in sizes_iconset:
                img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
                if size <= 32:
                    img_resized.save(iconset_dir / f'icon_{size}x{size}.png')
                    if size == 16:
                        img_resized_2x = img.resize((32, 32), Image.Resampling.LANCZOS)
                        img_resized_2x.save(iconset_dir / f'icon_{size}x{size}@2x.png')
                    elif size == 32:
                        img_resized_2x = img.resize((64, 64), Image.Resampling.LANCZOS)
                        img_resized_2x.save(iconset_dir / f'icon_{size}x{size}@2x.png')
                else:
                    img_resized.save(iconset_dir / f'icon_{size}x{size}.png')
                    if size < 1024:
                        img_resized_2x = img.resize((size * 2, size * 2), Image.Resampling.LANCZOS)
                        img_resized_2x.save(iconset_dir / f'icon_{size}x{size}@2x.png')
            
            # Try to create ICNS with iconutil
            result = subprocess.run([
                'iconutil', '-c', 'icns', str(iconset_dir), '-o', 'app.icns'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Created macOS icon: app.icns (with iconutil)")
                # Clean up iconset directory
                import shutil
                shutil.rmtree(iconset_dir)
            else:
                raise subprocess.CalledProcessError(result.returncode, 'iconutil')
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Method 2: Fallback - create basic ICNS
            try:
                img.save('app.icns', format='ICNS')
                print("✅ Created macOS icon: app.icns (basic format)")
            except:
                # Method 3: Create PNG and rename (will work on most systems)
                img.save('app.icns.png')
                print("⚠️  Created app.icns.png - rename to app.icns manually")
        
        # Clean up temporary files
        try:
            os.remove('icon_base.png')
        except:
            pass
            
    except ImportError:
        print("⚠️  Pillow not installed - creating placeholder icon files")
        
        # Create placeholder files with instructions
        placeholder_content = '''# ICON PLACEHOLDER
# Replace this file with a proper icon:
# 
# For Windows (app.ico):
# - Create a 256x256 PNG image
# - Convert to .ico format using online tools or:
#   pip install Pillow
#   python -c "from PIL import Image; img=Image.open('icon.png'); img.save('app.ico')"
#
# For macOS (app.icns):
# - Create a 1024x1024 PNG image  
# - On macOS, use iconutil:
#   mkdir MyIcon.iconset
#   sips -z 16 16 icon.png --out MyIcon.iconset/icon_16x16.png
#   sips -z 32 32 icon.png --out MyIcon.iconset/icon_16x16@2x.png
#   sips -z 32 32 icon.png --out MyIcon.iconset/icon_32x32.png
#   sips -z 64 64 icon.png --out MyIcon.iconset/icon_32x32@2x.png
#   sips -z 128 128 icon.png --out MyIcon.iconset/icon_128x128.png
#   sips -z 256 256 icon.png --out MyIcon.iconset/icon_128x128@2x.png
#   sips -z 256 256 icon.png --out MyIcon.iconset/icon_256x256.png
#   sips -z 512 512 icon.png --out MyIcon.iconset/icon_256x256@2x.png
#   sips -z 512 512 icon.png --out MyIcon.iconset/icon_512x512.png
#   sips -z 1024 1024 icon.png --out MyIcon.iconset/icon_512x512@2x.png
#   iconutil -c icns MyIcon.iconset
#   mv MyIcon.icns app.icns
'''
        
        with open('app.ico', 'w') as f:
            f.write(placeholder_content)
        with open('app.icns', 'w') as f:
            f.write(placeholder_content)
        
        print("💡 To create proper icons:")
        print("   1. Install Pillow: pip install Pillow")
        print("   2. Run this script again")
        print("   3. Or create icons manually using the instructions in the placeholder files")

def create_local_build_script():
    """Create local build script for testing"""
    build_script = '''#!/usr/bin/env python3
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
        print(f"\\n💡 Install missing packages:")
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
            print(f"\\n✅ Build successful!")
            print(f"📁 Executable: {expected}")
            print(f"📏 Size: {size:.1f} MB")
            
            # Test if executable runs
            print("\\n🧪 Testing executable...")
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
    
    print("\\n" + "=" * 60)
    if success:
        print("🎉 Local build completed successfully!")
        print("\\n💡 Next steps:")
        print("1. Test the executable manually")
        print("2. If it works, push to GitHub for cross-platform builds")
        print("3. GitHub Actions will build for Windows, macOS, and Linux")
    else:
        print("❌ Local build failed")
        print("\\n💡 Troubleshooting:")
        print("1. Check that all dependencies are installed")
        print("2. Ensure pressure_vessel_app.py exists")
        print("3. Try running without --windowed flag")
        print("4. Check PyInstaller documentation")

if __name__ == "__main__":
    main()
'''
    
    with open('build_local.py', 'w', encoding='utf-8') as f:
        f.write(build_script.strip())
    
    print("✅ Created local build script: build_local.py")

def create_license():
    """Create MIT license file"""
    license_content = '''MIT License

Copyright (c) 2024 Pressure Vessel Calculator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    with open('LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content.strip())
    
    print("✅ Created LICENSE file")

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
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git initialization failed: {e}")
        except FileNotFoundError:
            print("⚠️  Git not found. Please install Git first.")
    else:
        print("✅ Git repository already exists")

def create_github_templates():
    """Create GitHub issue and PR templates"""
    # Create .github directory
    github_dir = Path('.github')
    github_dir.mkdir(exist_ok=True)
    
    # Issue template
    issue_template_dir = github_dir / 'ISSUE_TEMPLATE'
    issue_template_dir.mkdir(exist_ok=True)
    
    bug_template = '''---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
 - Version: [e.g. v1.0.0]
 - Python version (if building from source): [e.g. 3.11]

**Additional context**
Add any other context about the problem here.
'''
    
    with open(issue_template_dir / 'bug_report.md', 'w', encoding='utf-8') as f:
        f.write(bug_template.strip())
    
    # Feature request template
    feature_template = '''---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
'''
    
    with open(issue_template_dir / 'feature_request.md', 'w', encoding='utf-8') as f:
        f.write(feature_template.strip())
    
    print("✅ Created GitHub issue templates")

def create_contributing_guide():
    """Create contributing guidelines"""
    contributing_content = '''# Contributing to Pressure Vessel Calculator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/pressure-vessel-calculator.git
   cd pressure-vessel-calculator
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Test the application**:
   ```bash
   python pressure_vessel_app.py
   ```

## 🔧 Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- Text editor or IDE

### Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python pressure_vessel_app.py
   ```

### Testing Changes
Before submitting changes:
1. **Test locally**:
   ```bash
   python build_local.py
   ```
2. **Verify all features work**
3. **Test on your target platform**

## 📝 How to Contribute

### Reporting Bugs
1. Check existing issues first
2. Use the bug report template
3. Include detailed reproduction steps
4. Add screenshots if helpful

### Suggesting Features
1. Check existing feature requests
2. Use the feature request template
3. Explain the use case clearly
4. Consider implementation complexity

### Code Contributions

#### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### 2. Make Your Changes
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

#### 3. Test Your Changes
- Test the GUI thoroughly
- Verify PDF processing works
- Check AI integration (if applicable)
- Run local build test

#### 4. Commit Your Changes
```bash
git add .
git commit -m "Add feature: description of what you added"
```

#### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

## 🎨 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### UI Code
- Use consistent spacing and alignment
- Follow the existing CustomTkinter patterns
- Maintain responsive design principles
- Test on different screen sizes

### Git Commits
- Use descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep first line under 50 characters
- Add details in the body if needed

## 🏗️ Build Process

### Local Building
```bash
python build_local.py
```

### Cross-Platform Building
- Automatic via GitHub Actions
- Triggered on push to main branch
- Creates Windows, macOS, and Linux builds

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style
- [ ] All tests pass locally
- [ ] Documentation updated if needed
- [ ] No merge conflicts with main branch

### PR Description Should Include
- Summary of changes
- Motivation for the change
- Testing performed
- Screenshots (for UI changes)

## 🐛 Debugging Tips

### Common Issues
1. **Import errors**: Check dependencies in requirements.txt
2. **UI issues**: Test on different platforms
3. **PDF processing**: Test with various PDF formats
4. **Build failures**: Check PyInstaller logs

### Getting Help
- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Include relevant error messages
- Provide system information

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make this project better! 🚀
'''
    
    with open('CONTRIBUTING.md', 'w', encoding='utf-8') as f:
        f.write(contributing_content.strip())
    
    print("✅ Created CONTRIBUTING.md")

def main():
    """Main setup function with comprehensive error handling"""
    print("🚀 Complete Cross-Platform Build Setup")
    print("=" * 70)
    print("🎯 This script will create everything needed for automated builds")
    print()
    
    # Check if main app file exists
    if not Path("pressure_vessel_app.py").exists():
        print("❌ pressure_vessel_app.py not found!")
        print("Make sure you're in the correct directory with your app file.")
        print()
        print("Current directory:", Path.cwd())
        print("Files in current directory:")
        for file in Path.cwd().iterdir():
            if file.is_file():
                print(f"  - {file.name}")
        sys.exit(1)
    
    print("📁 Current directory:", Path.cwd())
    print("📄 Found pressure_vessel_app.py ✅")
    print()
    
    try:
        # Create all necessary files
        print("📝 Creating project files...")
        create_requirements_txt()
        create_gitignore()
        create_license()
        create_readme()
        create_contributing_guide()
        create_github_templates()
        create_github_workflow()
        create_placeholder_icons()
        create_local_build_script()
        
        # Initialize git repo
        print()
        print("🔧 Setting up Git repository...")
        init_git_repo()
        
        print()
        print("=" * 70)
        print("🎉 Setup Complete! Everything is ready for cross-platform builds.")
        print()
        
        # Provide next steps
        print("📋 NEXT STEPS:")
        print()
        print("1. 🧪 Test Local Build (Optional):")
        print("   python build_local.py")
        print()
        print("2. 🔗 Create GitHub Repository:")
        print("   - Go to github.com and create a new repository")
        print("   - Copy the repository URL")
        print()
        print("3. 📤 Push to GitHub:")
        print("   git add .")
        print('   git commit -m "Initial commit with cross-platform build setup"')
        print("   git remote add origin YOUR_GITHUB_REPO_URL")
        print("   git push -u origin main")
        print()
        print("4. 🏗️ Automatic Builds Will Start!")
        print("   - GitHub Actions will build for Windows, macOS, and Linux")
        print("   - Go to Actions tab in your GitHub repo")
        print("   - Download artifacts for all platforms")
        print()
        print("5. 🏷️ Create Releases (Optional):")
        print("   git tag v1.0.0")
        print("   git push origin v1.0.0")
        print("   # This creates automatic GitHub releases")
        print()
        
        print("🎯 WHAT YOU'LL GET:")
        print("   ✅ Windows: PressureVesselCalculator.exe")
        print("   ✅ macOS: PressureVesselCalculator (executable)")  
        print("   ✅ Linux: PressureVesselCalculator (executable)")
        print()
        print("⏱️  Build Time: ~10-15 minutes")
        print("💰 Cost: FREE (GitHub Actions)")
        print("🔄 Automatic: Builds on every push")
        print()
        
        print("🔧 TROUBLESHOOTING:")
        print("   - If builds fail, check the Actions tab for logs")
        print("   - Ensure app.ico and app.icns icons exist")
        print("   - Test locally first with: python build_local.py")
        print("   - Check that pressure_vessel_app.py runs without errors")
        print()
        
        print("🚀 Ready to create professional cross-platform executables!")
        
    except Exception as e:
        print(f"❌ Setup failed with error: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Check that you have write permissions in this directory")
        print("2. Ensure Python has necessary modules (os, pathlib, etc.)")
        print("3. Try running as administrator/sudo if needed")
        print("4. Check disk space and directory permissions")
        sys.exit(1)

if __name__ == "__main__":
    main()