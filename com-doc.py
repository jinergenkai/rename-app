import win32com.client

# Khởi tạo Word
word = win32com.client.Dispatch("Word.Application")
word.Visible = False  # Ẩn cửa sổ Word

# Mở tài liệu
doc = word.Documents.Open(r"D:\project\rename-file\file-demo\111.doc")  # đổi path thật vào đây

# Duyệt qua từng đoạn (paragraph)
for i, para in enumerate(doc.Paragraphs):
    text = para.Range.Text.strip()
    if not text:
        continue  # Bỏ qua đoạn trắng

    font = para.Range.Font
    alignment = para.Alignment

    # In thông tin đoạn văn
    print(f"Paragraph {i+1}: {text}")
    print(f"  Font Name : {font.Name}")
    print(f"  Font Size : {font.Size}")
    print(f"  Bold      : {'Yes' if font.Bold else 'No'}")
    print(f"  Italic    : {'Yes' if font.Italic else 'No'}")
    
    align_map = {
        0: "Left", 1: "Center", 2: "Right", 3: "Justify"
    }
    print(f"  Alignment : {align_map.get(alignment, 'Unknown')}")
    print("-" * 40)

# Đóng tài liệu và Word
doc.Close(False)
word.Quit()

