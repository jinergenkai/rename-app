"""GUI components and event handlers."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional, Callable

from . import constants as c
from . import file_operations as fo

class FileRenamerUI:
    def __init__(self, root: tk.Tk):
        """Initialize the UI components."""
        self.root = root
        self.root.title(c.WINDOW_TITLE)
        self.root.geometry(c.WINDOW_SIZE)
        
        # Store current directory and preview mode
        self.current_directory: Optional[str] = None
        self.files: List[str] = []
        self.preview_mode = c.PREVIEW_FIRST_LINE
        
        self._create_directory_frame()
        self._create_supported_files_frame()
        self._create_files_frame()
        self._create_buttons_frame()
        self._create_pattern_frame()
        
    def _create_directory_frame(self) -> None:
        """Create the directory selection frame."""
        self.dir_frame = ttk.LabelFrame(
            self.root,
            text=c.DIRECTORY_FRAME_TEXT,
            padding="10"
        )
        self.dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dir_label = ttk.Label(self.dir_frame, text=c.NO_DIR_SELECTED)
        self.dir_label.pack(fill=tk.X)
        
    def _create_supported_files_frame(self) -> None:
        """Create frame showing supported file types."""
        self.supported_frame = ttk.LabelFrame(
            self.root,
            text=c.SUPPORTED_FILES_TEXT,
            padding="10"
        )
        self.supported_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create a text widget for better formatting
        supported_text = tk.Text(
            self.supported_frame,
            height=len(c.SUPPORTED_EXTENSIONS),
            wrap=tk.WORD,
            font=('TkDefaultFont', 9),
            relief=tk.FLAT,
            background=self.root.cget('bg')
        )
        supported_text.pack(fill=tk.X, padx=5)
        supported_text.insert('1.0', c.SUPPORTED_FILES_LIST)
        supported_text.configure(state='disabled')  # Make read-only
        
    def _create_files_frame(self) -> None:
        """Create the files list frame with treeview."""
        self.files_frame = ttk.LabelFrame(
            self.root,
            text=c.FILES_FRAME_TEXT,
            padding="10"
        )
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.files_frame,
            columns=(c.ORIGINAL_NAME_COL, c.NEW_NAME_COL, c.PREVIEW_COL),
            show="headings"
        )
        
        # Configure columns
        self.tree.heading(c.ORIGINAL_NAME_COL, text=c.ORIGINAL_NAME_COL)
        self.tree.heading(c.NEW_NAME_COL, text=c.NEW_NAME_COL)
        self.tree.heading(c.PREVIEW_COL, text=c.PREVIEW_COL)
        
        self.tree.column(c.ORIGINAL_NAME_COL, width=c.NAME_COL_WIDTH)
        self.tree.column(c.NEW_NAME_COL, width=c.NAME_COL_WIDTH)
        self.tree.column(c.PREVIEW_COL, width=c.PREVIEW_COL_WIDTH)
        
        # Add horizontal scrollbar for preview column
        h_scrollbar = ttk.Scrollbar(
            self.files_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
            self.files_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbars
        self.tree.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
    def _create_buttons_frame(self) -> None:
        """Create the buttons frame."""
        self.buttons_frame = ttk.Frame(self.root, padding="10")
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.load_btn = ttk.Button(
            self.buttons_frame,
            text=c.LOAD_DIR_BTN,
            command=self.load_files
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Add preview mode toggle button
        self.preview_mode_btn = ttk.Button(
            self.buttons_frame,
            text=c.PREVIEW_MODE_BTN,
            command=self.toggle_preview_mode
        )
        self.preview_mode_btn.pack(side=tk.LEFT, padx=5)
        
    def _create_pattern_frame(self) -> None:
        """Create the rename pattern frame."""
        self.pattern_frame = ttk.LabelFrame(
            self.root,
            text=c.RENAME_PATTERN_TEXT,
            padding="10"
        )
        self.pattern_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Prefix entry
        ttk.Label(self.pattern_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_var = tk.StringVar()
        self.prefix_entry = ttk.Entry(
            self.pattern_frame,
            textvariable=self.prefix_var
        )
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        
        # Suffix entry
        ttk.Label(self.pattern_frame, text="Suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_var = tk.StringVar()
        self.suffix_entry = ttk.Entry(
            self.pattern_frame,
            textvariable=self.suffix_var
        )
        self.suffix_entry.pack(side=tk.LEFT, padx=5)
        
        # Preview and Apply buttons
        self.preview_btn = ttk.Button(
            self.pattern_frame,
            text=c.PREVIEW_BTN,
            command=self.preview_changes
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.apply_btn = ttk.Button(
            self.pattern_frame,
            text=c.APPLY_BTN,
            command=self.apply_changes
        )
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        
    def toggle_preview_mode(self) -> None:
        """Toggle between preview modes."""
        current_index = c.PREVIEW_MODES.index(self.preview_mode)
        next_index = (current_index + 1) % len(c.PREVIEW_MODES)
        self.preview_mode = c.PREVIEW_MODES[next_index]
        # Refresh the preview if files are loaded
        if self.current_directory and self.files:
            self._update_tree_view(self.files)
        
    def load_files(self) -> None:
        """Load files from selected directory."""
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.current_directory = directory
            self.dir_label.config(text=directory)
            self.files = fo.get_files_in_directory(directory)
            self._update_tree_view(self.files)
            
    def preview_changes(self) -> None:
        """Preview filename changes."""
        if not self._validate_directory():
            return
            
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        
        self._update_tree_view(
            self.files,
            lambda f: fo.create_new_filename(f, prefix, suffix)
        )
            
    def apply_changes(self) -> None:
        """Apply the rename changes."""
        if not self._validate_directory():
            return
            
        try:
            # Get all files to rename
            files_to_rename = [
                (self.tree.item(item)["values"][0], self.tree.item(item)["values"][1])
                for item in self.tree.get_children()
            ]
            
            # Process files
            new_dir = fo.process_files(
                self.current_directory,
                files_to_rename,
                c.RENAMED_FILES_DIR
            )
            
            if any(old != new for old, new in files_to_rename):
                messagebox.showinfo(
                    "Success",
                    c.SUCCESS_MESSAGE.format(new_dir)
                )
            else:
                messagebox.showinfo("Info", c.NO_CHANGES_MESSAGE)
                
        except Exception as e:
            messagebox.showerror("Error", c.ERROR_MESSAGE.format(str(e)))
            
    def _validate_directory(self) -> bool:
        """Validate if directory is selected."""
        if not self.current_directory:
            messagebox.showwarning("Warning", c.WARNING_SELECT_DIR)
            return False
        return True
        
    def _update_tree_view(
        self,
        files: List[str],
        new_name_func: Optional[Callable[[str], str]] = None
    ) -> None:
        """Update the tree view with files."""
        self.tree.delete(*self.tree.get_children())
        is_multi_line = self.preview_mode == c.PREVIEW_MULTI_LINE
        
        for file in files:
            new_name = file if new_name_func is None else new_name_func(file)
            file_path = os.path.join(self.current_directory, file)
            preview = fo.get_file_preview(file_path, is_multi_line)
            self.tree.insert("", tk.END, values=(file, new_name, preview))