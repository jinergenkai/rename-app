"""Handle all file-related operations."""

import os
import shutil
from pathlib import Path
from typing import List, Tuple

def get_files_in_directory(directory: str) -> List[str]:
    """Get list of files in the specified directory."""
    return [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
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
    # Create new directory for renamed files
    new_dir = create_renamed_directory(current_dir, new_dir_name)
    
    # Copy files with new names
    for old_name, new_name in files_to_rename:
        if old_name != new_name:
            copy_file_with_new_name(current_dir, new_dir, old_name, new_name)
            
    return new_dir

def get_file_preview(file_path: str, max_chars: int) -> str:
    """Get a preview of the file's content."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
            # Replace newlines with spaces for single-line preview
            content = content.replace('\n', ' ').replace('\r', '')
            # Add ellipsis if content was truncated
            if f.read(1):  # Check if there's more content
                content += '...'
            return content
    except Exception:
        # Return placeholder for binary files or errors
        return "(Binary file or empty)"