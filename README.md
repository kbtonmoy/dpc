# 🚀 AI-Enhanced Pressure Vessel Cost Calculator

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