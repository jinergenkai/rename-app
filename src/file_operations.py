"""Handle all file-related operations."""

import os
import shutil
import re
from pathlib import Path
from typing import List, Tuple, Optional, Set, Dict

from . import constants as c
from . import ai_operations as ai

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

def clean_filename(text: str) -> str:
    """Convert text to valid filename."""
    # Remove invalid filename characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace whitespace sequences with single space
    text = re.sub(r'\s+', ' ', text.strip())
    # Truncate if too long
    if len(text) > c.MAX_FILENAME_LENGTH:
        text = text[:c.MAX_FILENAME_LENGTH].strip()
    return text or "untitled"

def handle_duplicate_name(name: str, ext: str, used_names: Set[str]) -> str:
    """Handle duplicate filenames by adding numbers."""
    base_name = name
    counter = 1
    new_name = f"{name}{ext}"
    
    while new_name.lower() in (n.lower() for n in used_names):
        name = f"{base_name} ({counter})"
        new_name = f"{name}{ext}"
        counter += 1
    
    used_names.add(new_name)
    return new_name

def create_content_based_filename(content: str, ext: str, used_names: Set[str]) -> str:
    """Create filename based on content preview."""
    # Get first line or chunk of content
    text = content.split('\n')[0] if '\n' in content else content
    # Clean and format the text
    filename = clean_filename(text)
    return handle_duplicate_name(filename, ext, used_names)

def create_ai_based_filename_and_summary(content: str, ext: str, used_names: Set[str]) -> Tuple[str, str]:
    """Create filename using AI and get summary."""
    try:
        suggested_name, summary = ai.generate_filename_and_summary(content)
        filename = clean_filename(suggested_name)
        return handle_duplicate_name(filename, ext, used_names), summary
    except Exception as e:
        raise Exception(f"{c.AI_ERROR.format(str(e))}")

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

def create_new_filename(
    filename: str,
    pattern: str,
    prefix: str = "",
    suffix: str = "",
    content: Optional[str] = None,
    used_names: Optional[Set[str]] = None,
    ai_summaries: Optional[Dict[str, str]] = None
) -> str:
    """Create new filename based on selected pattern."""
    if used_names is None:
        used_names = set()
        
    name, ext = os.path.splitext(filename)
    
    if pattern == c.PATTERN_CONTENT and content:
        return create_content_based_filename(content, ext, used_names)
    elif pattern == c.PATTERN_AI and content:
        if ai_summaries is not None:
            new_name, summary = create_ai_based_filename_and_summary(content, ext, used_names)
            ai_summaries[filename] = summary
            return new_name
        return handle_duplicate_name(f"{name}_ai", ext, used_names)
    elif pattern == c.PATTERN_PREFIX_SUFFIX:
        new_name = f"{prefix}{name}{suffix}"
        return handle_duplicate_name(new_name, ext, used_names)
    
    return filename

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
        return "Cần cài đặt python-docx để xem file docx"
    try:
        doc = docx.Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
        return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Không thể đọc file DOCX"

def get_doc_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of DOC file."""
    if not DOC_AVAILABLE:
        return "Cần cài đặt pywin32 để xem file doc"
    try:
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
        return process_text_for_preview(text, is_multi_line, max_lines)
    except Exception:
        return "Không thể đọc file DOC"

def get_excel_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of Excel file."""
    if not EXCEL_AVAILABLE:
        return "Cần cài đặt pandas và openpyxl/xlrd để xem file Excel"
    try:
        df = pd.read_excel(file_path, nrows=max_lines if is_multi_line else 1)
        preview = df.to_string(max_rows=max_lines if is_multi_line else 1)
        return process_text_for_preview(preview, is_multi_line, max_lines)
    except Exception:
        return "Không thể đọc file Excel"

def get_pdf_preview(file_path: str, is_multi_line: bool, max_lines: int) -> str:
    """Get preview of PDF file."""
    if not PDF_AVAILABLE:
        return "Cần cài đặt PyMuPDF hoặc pdfplumber để xem file PDF"
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
        return "Không thể đọc file PDF"

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
        return "Không thể đọc file văn bản"

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