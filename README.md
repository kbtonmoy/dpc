# 🚀 AI-Enhanced Pressure Vessel Cost Calculator

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