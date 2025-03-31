# Windows Development Guide

This guide provides detailed instructions for setting up and running the File Renamer Tool on Windows.

## Prerequisites

1. Install Python 3.8 or higher
   - Download from [Python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - Verify installation: `python --version`

2. Install Visual Studio Code (recommended)
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)
   - Install Python extension in VS Code

## Setup Instructions

### 1. Clone/Download the Project
- Create a project directory (e.g., `D:\project\rename-file`)
- Extract or clone project files into this directory

### 2. Set Up Virtual Environment

Open Command Prompt or PowerShell:
```powershell
# Navigate to project directory
cd D:\project\rename-file

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
# Install all required packages
pip install -r requirements.txt

# If pywin32 installation fails, install it separately
pip install pywin32
```

### 4. Run the Application

```powershell
# Make sure virtual environment is activated (.venv)
python -m src.main
```

## VS Code Integration

1. Open VS Code:
```powershell
code .
```

2. Select Python Interpreter:
   - Press `Ctrl + Shift + P`
   - Type "Python: Select Interpreter"
   - Choose the one in `.venv` folder

3. Configure VS Code settings:
   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
     "python.terminal.activateEnvironment": true,
     "files.exclude": {
       "**/__pycache__": true,
       "**/*.pyc": true
     }
   }
   ```

## File Support on Windows

### Word Documents (.docx, .doc)
- .docx: Requires python-docx (installed via requirements.txt)
- .doc: Requires both pywin32 AND Microsoft Word installed

### Excel Files (.xlsx, .xls)
- Requires pandas, openpyxl, and xlrd (installed via requirements.txt)
- No additional software needed

### PDF Files
- Uses PyMuPDF by default
- Falls back to pdfplumber if PyMuPDF fails
- No additional software needed

## Troubleshooting

### Common Issues

1. "python not found"
   - Check if Python is in PATH
   - Open System Properties > Environment Variables
   - Add Python paths if missing

2. "pip not found"
   - Run: `python -m ensurepip --upgrade`

3. pywin32 installation issues
   ```powershell
   # Try this if pip install fails
   python -m pip install --upgrade pywin32
   ```

4. Permission errors
   - Run Command Prompt as Administrator
   - Check folder permissions

5. Virtual Environment issues
   ```powershell
   # If activation fails, try:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Developer Tools

Recommended VS Code extensions for Python development:
- Python (Microsoft)
- Pylance
- Python Indent
- autoDocstring

### Testing File Operations

Test files location: `D:\project\rename-file\test_files`
```powershell
# Create test directory
mkdir test_files

# Create sample files
copy nul test_files\test.txt
copy nul test_files\test.docx
copy nul test_files\test.xlsx
```

## Updates and Maintenance

1. Update dependencies:
```powershell
pip list --outdated
pip install -r requirements.txt --upgrade
```

2. Clean project:
```powershell
# Remove cache files
del /s /q *.pyc
rmdir /s /q __pycache__

# Clean virtual environment
deactivate
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt