"""Constants used throughout the application."""

# Window settings
WINDOW_TITLE = "File Renamer Tool"
WINDOW_SIZE = "1000x600"  # Increased width for new column

# UI text
DIRECTORY_FRAME_TEXT = "Selected Directory"
NO_DIR_SELECTED = "No directory selected"
FILES_FRAME_TEXT = "Files to Rename"
RENAME_PATTERN_TEXT = "Rename Pattern"

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

# Messages
WARNING_SELECT_DIR = "Please select a directory first!"
SUCCESS_MESSAGE = "Files have been copied and renamed in:\n{}"
NO_CHANGES_MESSAGE = "No changes to apply."
ERROR_MESSAGE = "An error occurred: {}"

# Folder names
RENAMED_FILES_DIR = "renamed_files"

# Preview settings
PREVIEW_CHARS = 100  # Number of characters to show in preview
PREVIEW_PLACEHOLDER = "(Binary file or empty)"