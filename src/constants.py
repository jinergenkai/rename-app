"""Constants used throughout the application."""

# Window settings
WINDOW_TITLE = "File Renamer Tool"
WINDOW_SIZE = "1000x800"

# UI text
DIRECTORY_FRAME_TEXT = "Selected Directory"
NO_DIR_SELECTED = "No directory selected"
FILES_FRAME_TEXT = "Files to Rename"
RENAME_PATTERN_TEXT = "Rename Pattern"
SUPPORTED_FILES_TEXT = "Supported Files:"

# Column names
ORIGINAL_NAME_COL = "Original Name"
NEW_NAME_COL = "New Name"
PREVIEW_COL = "Content Preview"

# Column widths
NAME_COL_WIDTH = 250
PREVIEW_COL_WIDTH = 400

# Button texts
LOAD_DIR_BTN = "Load Directory"
PREVIEW_BTN = "Preview Changes"
APPLY_BTN = "Apply Changes"
PREVIEW_MODE_BTN = "Toggle Preview Mode"

# Messages
WARNING_SELECT_DIR = "Please select a directory first!"
SUCCESS_MESSAGE = "Files have been copied and renamed in:\n{}"
NO_CHANGES_MESSAGE = "No changes to apply."
ERROR_MESSAGE = "An error occurred: {}"
UNSUPPORTED_FILE = "(Unsupported file type)"

# Folder names
RENAMED_FILES_DIR = "renamed_files"

# Preview settings
PREVIEW_FIRST_LINE = "First Line"
PREVIEW_MULTI_LINE = "10 Lines"
PREVIEW_MODES = [PREVIEW_FIRST_LINE, PREVIEW_MULTI_LINE]
MAX_LINES_PREVIEW = 10
PREVIEW_PLACEHOLDER = "(Binary file or empty)"

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.docx': 'Word Document (*.docx)',
    '.doc': 'Word Document (*.doc)',
    '.xlsx': 'Excel Spreadsheet (*.xlsx)',
    '.xls': 'Excel Spreadsheet (*.xls)',
    '.pdf': 'PDF Document (*.pdf)',
    '.txt': 'Text File (*.txt)',
}

# Get formatted supported files text
SUPPORTED_FILES_LIST = "\n".join(
    f"• {desc}" for desc in SUPPORTED_EXTENSIONS.values()
)

# Error messages
MISSING_DEPS_MESSAGE = """
Missing required dependencies for file preview.
Please install the following:

For .docx files:
    pip install python-docx

For .doc files (Windows):
    pip install pywin32

For Excel files:
    pip install pandas openpyxl xlrd

For PDF files:
    pip install pymupdf pdfplumber
"""