"""Constants used throughout the application."""

# Window settings
WINDOW_TITLE = "Công Cụ Đổi Tên Tập Tin"
WINDOW_SIZE = "1300x700"

# Step instructions
INSTRUCTION_TEXT = """Các bước thực hiện:
1. Chọn thư mục chứa tập tin cần đổi tên
2. Chọn cách đổi tên:
   • Dùng Nội Dung: Tự động dùng nội dung của file
   • AI Tóm Tắt: Sử dụng AI để tạo tên thông minh
   • Tiền Tố/Hậu Tố: Thêm tiền tố hoặc hậu tố vào tên cũ
3. Nhấn "Xem Trước" để kiểm tra kết quả
4. Nhấn "Áp Dụng" để hoàn tất đổi tên
==========================
*** Lưu ý khi thay đổi Tùy Chọn mà xảy ra lỗi -> vui lòng chọn lại thư mục cần đổi tên"""

# UI text
INSTRUCTION_FRAME_TEXT = "Hướng Dẫn Sử Dụng"
DIRECTORY_FRAME_TEXT = "Thư Mục Đã Chọn"
NO_DIR_SELECTED = "Chưa chọn thư mục"
FILES_FRAME_TEXT = "Danh Sách Tập Tin"
RENAME_PATTERN_TEXT = "Tùy Chọn Đổi Tên"
SUPPORTED_FILES_TEXT = "Định Dạng Hỗ Trợ:"
PREVIEW_OPTIONS_TEXT = "Tùy Chọn Xem Trước"
PREVIEW_LINES_LABEL = "Số dòng xem trước:"
API_KEY_BUTTON = "Nhập API Key"
API_KEY_PROMPT = "Nhập OpenAI API Key:"
API_KEY_SAVED = "✓ Đã lưu API Key"
API_KEY_REQUIRED = "⚠ Cần có API Key để sử dụng tính năng AI"
CONSOLE_TEXT = "Thông Báo Hệ Thống"

# Confirmation messages
CONFIRM_APPLY = "Xác nhận áp dụng thay đổi?"
CONFIRM_APPLY_DETAIL = "Bạn có chắc chắn muốn đổi tên các tập tin đã chọn?\nCác tập tin gốc sẽ được giữ nguyên."

# Log levels and formats
LOG_INFO = "[INFO]"
LOG_ERROR = "[LỖI]"
LOG_TIME_FORMAT = "%H:%M:%S"

# Rename patterns
PATTERN_CONTENT = "Dùng Nội Dung"
PATTERN_AI = "AI Tóm Tắt"
PATTERN_PREFIX_SUFFIX = "Tiền Tố/Hậu Tố"
PATTERN_OPTIONS = [
    PATTERN_CONTENT,
    PATTERN_PREFIX_SUFFIX
]

# AI settings
OPENAI_MODEL = "gpt-3.5-turbo"
MAX_CONTENT_CHARS = 1000
AI_PROMPT = """
Dựa vào nội dung sau, hãy tạo một tên tập tin ngắn gọn (tối đa 100 ký tự) mô tả chính xác nội dung. Chỉ trả về tên tập tin (không kèm đuôi file), không kèm giải thích.

Nội dung:
{content}
"""

AI_SUMMARY_PROMPT = """
Tóm tắt ngắn gọn nội dung sau trong 100 ký tự:

{content}
"""

# Column names
ORIGINAL_NAME_COL = "Tên Gốc"
NEW_NAME_COL = "Tên Mới"
PREVIEW_COL = "Xem Trước Nội Dung"
AI_SUMMARY_COL = "Tóm Tắt AI"

# Column widths
NAME_COL_WIDTH = 200
PREVIEW_COL_WIDTH = 300
AI_SUMMARY_COL_WIDTH = 200

# Button texts
LOAD_DIR_BTN = "Chọn Thư Mục"
PREVIEW_BTN = "Xem Trước"
APPLY_BTN = "Áp Dụng"

# Messages
WARNING_SELECT_DIR = "⚠ Vui lòng chọn thư mục trước!"
SUCCESS_MESSAGE = "✓ Đã đổi tên tập tin thành công tại:\n{}"
NO_CHANGES_MESSAGE = "ℹ Không có thay đổi nào."
ERROR_MESSAGE = "⚠ Đã xảy ra lỗi: {}"
UNSUPPORTED_FILE = "(Định dạng không được hỗ trợ)"
AI_ERROR = "⚠ Lỗi AI: {}"
AI_WAITING = "⏳ Đang xử lý AI..."
AI_SUCCESS = "✓ Đã tạo tên bằng AI"
FILE_ERROR = "⚠ Lỗi đọc tập tin: {}"

# Folder names
RENAMED_FILES_DIR = "renamed_files"

# Preview settings
PREVIEW_PLACEHOLDER = "(Tập tin trống hoặc không đọc được)"
MAX_FILENAME_LENGTH = 200

# Config file
CONFIG_FILE = ".config"
API_KEY_FILE = ".apikey"

# Supported file extensions with Vietnamese descriptions
SUPPORTED_EXTENSIONS = {
    '.docx': 'Tài liệu Word (*.docx)',
    '.doc': 'Tài liệu Word cũ (*.doc)',
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
"""