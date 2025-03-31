# File Renamer Tool

A simple Python GUI application to rename multiple files with prefix/suffix in a selected directory.

## Quick Start

**Windows Users**: See [WINDOWS.md](WINDOWS.md) for detailed Windows-specific setup and development instructions.

## Supported File Types

The tool supports previewing and renaming the following file types:
- `.docx` - Word Documents
- `.doc` - Legacy Word Documents (Windows only)
- `.xlsx` - Excel Spreadsheets
- `.xls` - Legacy Excel Spreadsheets
- `.pdf` - PDF Documents
- `.txt` - Text Files

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- virtualenv or venv module

### 2. Create and Activate Virtual Environment

#### Windows
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

#### Linux/MacOS
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Make sure your virtual environment is activated
python -m src.main
```

To deactivate the virtual environment when you're done:
```bash
deactivate
```

## Project Structure
```
.venv/              # Virtual environment directory
src/
├── __init__.py     # Package initialization
├── constants.py    # Application constants
├── file_operations.py   # File handling operations
├── main.py        # Main entry point
└── ui.py          # GUI components
requirements.txt    # Project dependencies
WINDOWS.md         # Windows-specific documentation
```

## Features
- Select directory to rename supported files
- Add prefix and/or suffix to filenames
- Preview file contents before renaming
- Preview changes before applying
- Creates copies in a new "renamed_files" directory (keeps originals intact)
- Simple and intuitive interface

## How to Use

1. Click "Load Directory" to select the folder containing files to rename
2. Enter desired prefix and/or suffix
3. View file contents in the preview column
4. Click "Preview Changes" to see how files will be renamed
5. Click "Apply Changes" to create renamed copies in a new "renamed_files" folder

## Notes
- Original files remain unchanged
- New files are created in a "renamed_files" subdirectory
- File extensions are preserved during renaming
- Preview requires appropriate dependencies for each file type
- Missing dependencies will show installation instructions in preview

## Basic Troubleshooting

For detailed troubleshooting:
- Windows users: See [WINDOWS.md](WINDOWS.md)
- Linux/MacOS users: Create an issue if you encounter problems

### Missing Dependencies
If you see "Install [package] for [file type] preview" messages:
1. Make sure your virtual environment is activated
2. Run `pip install -r requirements.txt` again

### Permission Issues
- Make sure you have read/write permissions in the directory
- Run the application with appropriate permissions

### Preview Not Working
- Check if the required dependencies are installed
- Verify that the file isn't corrupted
- For .doc files on Windows, ensure MS Word is installed