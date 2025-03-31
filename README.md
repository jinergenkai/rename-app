# File Renamer Tool

A simple Python GUI application to rename multiple files with prefix/suffix in a selected directory.

## Project Structure

```
src/
├── __init__.py      # Package initialization
├── constants.py     # Application constants
├── file_operations.py   # File handling operations
├── main.py         # Main entry point
└── ui.py           # GUI components
```

## Features
- Select directory to rename files
- Add prefix and/or suffix to filenames
- Preview changes before applying
- Creates copies in a new "renamed_files" directory (keeps originals intact)
- Simple and intuitive interface

## Requirements
- Python 3.x
- tkinter (usually comes with Python)

## How to Run

1. Make sure you have Python installed
2. Navigate to the project directory
3. Run the application:
```bash
python -m src.main
```

## How to Use

1. Click "Load Directory" to select the folder containing files to rename
2. Enter desired prefix and/or suffix
3. Click "Preview Changes" to see how files will be renamed
4. Click "Apply Changes" to create renamed copies in a new "renamed_files" folder

## Notes
- Original files remain unchanged
- New files are created in a "renamed_files" subdirectory
- File extensions are preserved during renaming