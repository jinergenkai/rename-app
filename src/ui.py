"""GUI components and event handlers."""

import os
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional, Callable, Dict, Set

from . import constants as c
from . import file_operations as fo

class FileRenamerUI:
    def __init__(self, root: tk.Tk):
        """Initialize the UI components."""
        self.root = root
        self.root.title(c.WINDOW_TITLE)
        self.root.geometry(c.WINDOW_SIZE)
        
        # Store current directory and preview lines
        self.current_directory: Optional[str] = None
        self.files: List[str] = []
        self.preview_lines = tk.StringVar(value=str(c.DEFAULT_PREVIEW_LINES))
        
        # Initialize with content pattern
        self.pattern = tk.StringVar(value=c.PATTERN_CONTENT)
        
        # Store file previews to avoid reloading
        self.preview_cache: Dict[str, str] = {}
        
        # Track used filenames
        self.used_names: Set[str] = set()
        
        self._create_directory_frame()
        self._create_options_frame()
        self._create_files_frame()
        self._create_rename_frame()
        self._create_progress_frame()
        
        # Hide prefix/suffix frame by default since we're using content pattern
        self.prefix_suffix_frame.pack_forget()
        
    def _create_directory_frame(self) -> None:
        """Create the directory selection frame."""
        self.dir_frame = ttk.LabelFrame(
            self.root,
            text=c.DIRECTORY_FRAME_TEXT,
            padding="10"
        )
        self.dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add Load Directory button first
        self.load_btn = ttk.Button(
            self.dir_frame,
            text=c.LOAD_DIR_BTN,
            command=self.load_files
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Add directory label
        self.dir_label = ttk.Label(self.dir_frame, text=c.NO_DIR_SELECTED)
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
    def _create_options_frame(self) -> None:
        """Create frame for preview options and supported files."""
        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Preview options on the left
        preview_frame = ttk.LabelFrame(
            options_frame,
            text=c.PREVIEW_OPTIONS_TEXT,
            padding="10"
        )
        preview_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Number of lines entry
        ttk.Label(
            preview_frame,
            text=c.PREVIEW_LINES_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        vcmd = (self.root.register(self._validate_number), '%P')
        self.preview_lines_entry = ttk.Entry(
            preview_frame,
            textvariable=self.preview_lines,
            width=5,
            validate='all',
            validatecommand=vcmd
        )
        self.preview_lines_entry.pack(side=tk.LEFT, padx=5)
        
        # Supported files on the right
        self.supported_frame = ttk.LabelFrame(
            options_frame,
            text=c.SUPPORTED_FILES_TEXT,
            padding="10"
        )
        self.supported_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
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
        
    def _create_rename_frame(self) -> None:
        """Create the rename options frame."""
        self.rename_frame = ttk.LabelFrame(
            self.root,
            text=c.RENAME_PATTERN_TEXT,
            padding="10"
        )
        self.rename_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Pattern selection
        pattern_frame = ttk.Frame(self.rename_frame)
        pattern_frame.pack(fill=tk.X, pady=5)
        
        for pattern in c.PATTERN_OPTIONS:
            ttk.Radiobutton(
                pattern_frame,
                text=pattern,
                value=pattern,
                variable=self.pattern,
                command=self._on_pattern_change
            ).pack(side=tk.LEFT, padx=10)
        
        # Prefix/Suffix frame (hidden by default)
        self.prefix_suffix_frame = ttk.Frame(self.rename_frame)
        
        # Prefix entry
        ttk.Label(self.prefix_suffix_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_var = tk.StringVar()
        self.prefix_entry = ttk.Entry(
            self.prefix_suffix_frame,
            textvariable=self.prefix_var
        )
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        
        # Suffix entry
        ttk.Label(self.prefix_suffix_frame, text="Suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_var = tk.StringVar()
        self.suffix_entry = ttk.Entry(
            self.prefix_suffix_frame,
            textvariable=self.suffix_var
        )
        self.suffix_entry.pack(side=tk.LEFT, padx=5)
        
        # Preview and Apply buttons
        self.preview_btn = ttk.Button(
            self.rename_frame,
            text=c.PREVIEW_BTN,
            command=self.preview_changes
        )
        self.preview_btn.pack(side=tk.RIGHT, padx=5)
        
        self.apply_btn = ttk.Button(
            self.rename_frame,
            text=c.APPLY_BTN,
            command=self.apply_changes
        )
        self.apply_btn.pack(side=tk.RIGHT, padx=5)
        
    def _on_pattern_change(self) -> None:
        """Handle pattern selection change."""
        pattern = self.pattern.get()
        
        # Show/hide prefix/suffix inputs
        if pattern == c.PATTERN_PREFIX_SUFFIX:
            self.prefix_suffix_frame.pack(fill=tk.X, pady=5)
        else:
            self.prefix_suffix_frame.pack_forget()
            
        # Update preview if files are loaded
        if self.files:
            self.preview_changes()
            
    def _create_progress_frame(self) -> None:
        """Create progress bar frame."""
        self.progress_frame = ttk.Frame(self.root, padding="5")
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_var = tk.StringVar(value="")
        self.progress_label = ttk.Label(
            self.progress_frame,
            textvariable=self.progress_var
        )
        self.progress_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=200
        )
        
    def _validate_number(self, value: str) -> bool:
        """Validate the preview lines entry."""
        if value == "":
            return True
        try:
            num = int(value)
            if 1 <= num <= c.MAX_PREVIEW_LINES:
                self._refresh_previews()
                return True
            return False
        except ValueError:
            return False
            
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
        
    def load_files(self) -> None:
        """Load files from selected directory."""
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.current_directory = directory
            self.dir_label.config(text=directory)
            self.files = fo.get_files_in_directory(directory)
            self.preview_cache.clear()
            self.used_names.clear()
            
            # Show progress bar
            self.progress_bar.pack(side=tk.LEFT, padx=5)
            self.progress_bar["maximum"] = len(self.files)
            self.progress_bar["value"] = 0
            
            # Start loading files
            self.tree.delete(*self.tree.get_children())
            self._load_next_file(0)
            
    def _load_next_file(self, index: int) -> None:
        """Load next file and its preview."""
        if index >= len(self.files):
            # Done loading
            self.progress_var.set("Loading complete")
            self.progress_bar.pack_forget()
            # Auto-preview with content pattern
            self.preview_changes()
            return
            
        file = self.files[index]
        file_path = os.path.join(self.current_directory, file)
        
        try:
            preview_lines = int(self.preview_lines.get())
        except ValueError:
            preview_lines = c.DEFAULT_PREVIEW_LINES
            
        # Update progress
        self.progress_var.set(f"Loading {index + 1}/{len(self.files)}: {file}")
        self.progress_bar["value"] = index + 1
        
        # Get preview and add to tree
        preview = fo.get_file_preview(file_path, preview_lines > 1, preview_lines)
        self.preview_cache[file] = preview
        self.tree.insert("", tk.END, values=(file, file, preview))
        
        # Schedule next file load
        self.root.after(10, self._load_next_file, index + 1)
            
    def _refresh_previews(self) -> None:
        """Refresh all file previews with new line count."""
        if not self.current_directory or not self.files:
            return
            
        self.preview_cache.clear()
        self.used_names.clear()
        self._update_tree_view(self.files)
            
    def preview_changes(self) -> None:
        """Preview filename changes."""
        if not self._validate_directory():
            return
            
        pattern = self.pattern.get()
        if pattern == c.PATTERN_AI:
            messagebox.showinfo("Info", c.AI_NOT_AVAILABLE)
            return

        # Clear used names for new preview
        self.used_names.clear()
        self._update_tree_view(self.files)
            
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
        pattern = self.pattern.get()
        
        for file in files:
            preview = self.preview_cache.get(file, "Loading...")
            
            if pattern == c.PATTERN_PREFIX_SUFFIX:
                new_name = fo.create_new_filename(
                    file,
                    pattern,
                    self.prefix_var.get(),
                    self.suffix_var.get(),
                    used_names=self.used_names
                )
            elif pattern == c.PATTERN_CONTENT:
                new_name = fo.create_new_filename(
                    file,
                    pattern,
                    content=preview,
                    used_names=self.used_names
                )
            else:  # AI pattern (future implementation)
                new_name = file
                
            self.tree.insert("", tk.END, values=(file, new_name, preview))