"""Handle all file-related operations."""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Optional

from . import constants as c

# Optional imports for different file types
try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import win32com.client
    DOC_AVAILABLE = True
except ImportError:
    DOC_AVAILABLE = False

try:
    import pandas as pd
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False

def process_text_for_preview(text: str, is_multi_line: bool = False, max_lines: int = 1) -> str:
    """Process text for preview display."""
    if not text:
        return ""
        
    # Split into lines and remove empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    if not lines:
        return ""
        
    if is_multi_line:
        # Get up to max_lines lines and join with spaces
        preview_lines = lines[:max_lines]
        return " ".join(preview_lines)
    else:
        # Return just the first line
        return lines[0]

def get_files_in_directory(directory: str) -> List[str]:
    """Get list of supported files in the specified directory."""
    return [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and os.path.splitext(f)[1].lower() in c.SUPPORTED_EXTENSIONS
    ]

def create_new_filename(filename: str, prefix: str = "", suffix: str = "") -> str:
    """Create new filename with prefix and suffix."""
    name, ext = os.path.splitext(filename)
    return f"{prefix}{name}{suffix}{ext}"

def create_renamed_directory(base_dir: str, new_dir_name: str) -> str:
    """Create directory for renamed files."""
    new_dir = os.path.join(base_dir, new_dir_name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    return new_dir

def copy_file_with_new_name(
    source_dir: str,
    dest_dir: str,
    old_name: str,
    new_name: str
) -> None:
    """Copy a file with a new name to destination directory."""
    old_path = os.path.join(source_dir, old_name)
    new_path = os.path.join(dest_dir, new_name)
    shutil.copy2(old_path, new_path)

def process_files(
    current_dir: str,
    files_to_rename: List[Tuple[str, str]],
    new_dir_name: str
) -> str:
    """Process files and return the path to renamed files."""
    new_dir = create_renamed_directory(current_dir, new_dir_name)
    for old_name, new_name in files_to_rename:
        if old_name != new_name:
            copy_file_with_new_name(current_dir, new_dir, old_name, new_name)
    return new_dir

def get_docx_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of DOCX file."""
    if not DOCX_AVAILABLE:
        return "Install python-docx for .docx preview"
    try:
        doc = docx.Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
        return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Unable to read DOCX file"

def get_doc_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of DOC file."""
    if not DOC_AVAILABLE:
        return "Install pywin32 for .doc preview"
    try:
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
        return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Unable to read DOC file"

def get_excel_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of Excel file."""
    if not EXCEL_AVAILABLE:
        return "Install pandas and openpyxl/xlrd for Excel preview"
    try:
        df = pd.read_excel(file_path, nrows=max_lines if is_multi_line else 1)
        preview = df.to_string(max_rows=max_lines if is_multi_line else 1)
        return process_text_for_preview(preview, is_multi_line, max_lines)
    except Exception:
        return "Unable to read Excel file"

def get_pdf_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of PDF file."""
    if not PDF_AVAILABLE:
        return "Install PyMuPDF or pdfplumber for PDF preview"
    try:
        text = ""
        try:
            with fitz.open(file_path) as pdf:
                text = pdf[0].get_text()
        except NameError:
            with pdfplumber.open(file_path) as pdf:
                text = pdf.pages[0].extract_text()
        return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Unable to read PDF file"

def get_text_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of text file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            if is_multi_line:
                lines = []
                for _ in range(max_lines):
                    line = f.readline()
                    if not line:
                        break
                    lines.append(line)
                text = "".join(lines)
            else:
                text = f.readline()
            return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Unable to read text file"

def get_file_preview(file_path: str, is_multi_line: bool = False, max_lines: int = 1) -> str:
    """Get a preview of the file's content based on file type."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext not in c.SUPPORTED_EXTENSIONS:
        return c.UNSUPPORTED_FILE
        
    preview_functions = {
        '.docx': get_docx_preview,
        '.doc': get_doc_preview,
        '.xlsx': get_excel_preview,
        '.xls': get_excel_preview,
        '.pdf': get_pdf_preview,
        '.txt': get_text_preview,
    }
    
    preview_func = preview_functions.get(ext, get_text_preview)
    return preview_func(file_path, is_multi_line, max_lines)