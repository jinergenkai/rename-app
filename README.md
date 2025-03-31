# Công Cụ Đổi Tên Tập Tin

Ứng dụng GUI đơn giản để đổi tên nhiều tập tin dựa trên nội dung.

## Tính Năng

1. Tùy chọn đổi tên:
   - **Dùng Nội Dung**: Dùng nội dung tập tin làm tên (mặc định)
   - **AI Tóm Tắt**: Dùng AI để tạo tên tập tin (sắp có)
   - **Tiền Tố/Hậu Tố**: Thêm tiền tố hoặc hậu tố vào tên

2. Định dạng hỗ trợ:
   - `.docx` - Tài liệu Word
   - `.doc` - Tài liệu Word cũ (Windows)
   - `.xlsx` - Bảng tính Excel
   - `.xls` - Bảng tính Excel cũ
   - `.pdf` - Tài liệu PDF
   - `.txt` - Văn bản

## Cài Đặt

### 1. Yêu cầu hệ thống
- Python 3.8 trở lên
- virtualenv hoặc venv module

### 2. Tạo môi trường ảo

#### Windows
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường
.venv\Scripts\activate
```

#### Linux/MacOS
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường
source .venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
# Cài đặt các gói cần thiết
pip install -r requirements.txt
```

### 4. Chạy ứng dụng
```bash
# Đảm bảo môi trường ảo đã được kích hoạt
python -m src.main
```

Để tắt môi trường ảo:
```bash
deactivate
```

## Cấu Trúc Dự Án
```
.venv/              # Thư mục môi trường ảo
src/
├── __init__.py     # Khởi tạo package
├── constants.py    # Các hằng số
├── file_operations.py   # Xử lý tập tin
├── main.py        # Điểm vào chương trình
└── ui.py          # Giao diện người dùng
requirements.txt    # Các thư viện cần thiết
```

## Cách Sử Dụng

1. Nhấn "Chọn Thư Mục" để chọn thư mục chứa tập tin cần đổi tên
2. Chọn số dòng xem trước (1-50)
3. Chọn kiểu đổi tên:
   - Dùng Nội Dung: Tự động dùng nội dung tập tin
   - AI Tóm Tắt: (Sắp có)
   - Tiền Tố/Hậu Tố: Thêm tiền tố hoặc hậu tố vào tên cũ
4. Nhấn "Xem Trước" để xem kết quả
5. Nhấn "Áp Dụng" để tạo bản sao với tên mới

## Lưu Ý
- Tập tin gốc được giữ nguyên
- Tập tin mới được tạo trong thư mục "renamed_files"
- Phần mở rộng tập tin được giữ nguyên
- Cần cài đặt thư viện tương ứng cho mỗi loại tập tin
- Tên tập tin trùng sẽ tự động thêm số (1), (2),...

## Xử Lý Sự Cố

### Thiếu thư viện
Nếu thấy thông báo "Cần cài đặt...":
1. Đảm bảo môi trường ảo đã được kích hoạt
2. Chạy lại `pip install -r requirements.txt`

### Lỗi quyền truy cập
- Đảm bảo có quyền đọc/ghi trong thư mục
- Chạy ứng dụng với quyền phù hợp

### Xem trước không hoạt động
- Kiểm tra thư viện cần thiết đã được cài đặt
- Kiểm tra tập tin có bị hỏng không
- Với file .doc trên Windows, cần cài Microsoft Word

## Tạo File Thực Thi (EXE)

Để tạo file thực thi độc lập cho Windows:

1. Đảm bảo đã cài đặt môi trường và các thư viện:
```bash
# Kích hoạt môi trường ảo
.venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

2. Tạo file exe bằng PyInstaller:
```bash
# Di chuyển vào thư mục gốc của dự án
# Tạo file exe với các tùy chọn cần thiết
pyinstaller --name "RenameFiles" ^
            --icon "src/assets/icon.ico" ^
            --windowed ^
            --add-data "src;src" ^
            --noconfirm ^
            "src/main.py"
```

File thực thi sẽ được tạo trong thư mục `dist/RenameFiles`.

Các tùy chọn PyInstaller:
- `--name`: Tên file thực thi
- `--icon`: Icon cho ứng dụng (tùy chọn)
- `--windowed`: Không hiện cửa sổ console
- `--add-data`: Thêm các file/thư mục cần thiết
- `--noconfirm`: Không hỏi xác nhận khi ghi đè

3. Chạy file thực thi:
- Mở thư mục `dist/RenameFiles`
- Chạy file `RenameFiles.exe`

Lưu ý:
- Đảm bảo tất cả thư viện cần thiết đã được cài đặt trước khi tạo file exe
- Có thể cần thêm tùy chọn `--hidden-import` nếu có thư viện không được tự động phát hiện