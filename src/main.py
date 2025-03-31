"""Main entry point for the File Renamer application."""

import os
import sys
import tkinter as tk
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from src.ui import FileRenamerUI

def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = FileRenamerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()