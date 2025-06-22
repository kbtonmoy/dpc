# Contributing to Pressure Vessel Calculator

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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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