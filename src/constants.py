"""Constants used throughout the application."""

# Window settings
WINDOW_TITLE = "Công Cụ Đổi Tên Tập Tin"
WINDOW_SIZE = "1000x900"

# UI text
DIRECTORY_FRAME_TEXT = "Thư Mục Đã Chọn"
NO_DIR_SELECTED = "Chưa chọn thư mục"
FILES_FRAME_TEXT = "Danh Sách Tập Tin"
RENAME_PATTERN_TEXT = "Tùy Chọn Đổi Tên"
SUPPORTED_FILES_TEXT = "Định Dạng Hỗ Trợ:"
PREVIEW_OPTIONS_TEXT = "Tùy Chọn Xem Trước"
PREVIEW_LINES_LABEL = "Số dòng xem trước:"

# Rename patterns
PATTERN_CONTENT = "Dùng Nội Dung"
PATTERN_AI = "AI Tóm Tắt (Sắp Có)"
PATTERN_PREFIX_SUFFIX = "Tiền Tố/Hậu Tố"
PATTERN_OPTIONS = [
    PATTERN_CONTENT,
    PATTERN_AI,
    PATTERN_PREFIX_SUFFIX
]

# Column names
ORIGINAL_NAME_COL = "Tên Gốc"
NEW_NAME_COL = "Tên Mới"
PREVIEW_COL = "Xem Trước Nội Dung"

# Column widths
NAME_COL_WIDTH = 250
PREVIEW_COL_WIDTH = 400

# Button texts
LOAD_DIR_BTN = "Chọn Thư Mục"
PREVIEW_BTN = "Xem Trước"
APPLY_BTN = "Áp Dụng"

# Messages
WARNING_SELECT_DIR = "Vui lòng chọn thư mục trước!"
SUCCESS_MESSAGE = "Đã đổi tên tập tin thành công tại:\n{}"
NO_CHANGES_MESSAGE = "Không có thay đổi nào."
ERROR_MESSAGE = "Đã xảy ra lỗi: {}"
UNSUPPORTED_FILE = "(Định dạng không được hỗ trợ)"
AI_NOT_AVAILABLE = "Tính năng AI chưa khả dụng"

# Folder names
RENAMED_FILES_DIR = "renamed_files"

# Preview settings
DEFAULT_PREVIEW_LINES = 1
MAX_PREVIEW_LINES = 50
PREVIEW_PLACEHOLDER = "(Tập tin trống hoặc không đọc được)"
MAX_FILENAME_LENGTH = 200

# Supported file extensions with Vietnamese descriptions
SUPPORTED_EXTENSIONS = {
    '.docx': 'Tài liệu Word (*.docx)',
    '.doc': 'Tài liệu Word cũ (*.doc)',
    '.xlsx': 'Bảng tính Excel (*.xlsx)',
    '.xls': 'Bảng tính Excel cũ (*.xls)',
    '.pdf': 'Tài liệu PDF (*.pdf)',
    '.txt': 'Văn bản (*.txt)',
}

# Get formatted supported files text
SUPPORTED_FILES_LIST = "\n".join(
    f"• {desc}" for desc in SUPPORTED_EXTENSIONS.values()
)

# Error messages
MISSING_DEPS_MESSAGE = """
Thiếu các thư viện cần thiết.
Vui lòng cài đặt:

Cho file .docx:
    pip install python-docx

Cho file .doc (Windows):
    pip install pywin32

Cho file Excel:
    pip install pandas openpyxl xlrd

Cho file PDF:
    pip install pymupdf pdfplumber
"""