"""GUI components and event handlers."""

import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from typing import List, Optional, Callable, Dict, Set

from . import constants as c
from . import file_operations as fo
from . import core

class FileRenamerUI:
    def __init__(self, root: tk.Tk):
        """Initialize the UI components."""
        self.root = root
        self.root.title(c.WINDOW_TITLE)
        self.root.state('zoomed')
        
        # Create main container with left and right panes
        self.main_container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left pane for main UI
        self.left_pane = ttk.Frame(self.main_container)
        self.main_container.add(self.left_pane, weight=3)
        
        # Right pane for console
        self.right_pane = ttk.Frame(self.main_container)
        self.main_container.add(self.right_pane, weight=1)
        
        # Store current directory
        self.current_directory: Optional[str] = None
        self.files: List[str] = []
        self.match_keywords = []
        self.ignore_keywords = []
        
        # Track used filenames
        self.used_names: Set[str] = set()
        
        # Initialize UI components
        self._create_instruction_frame()
        self._create_directory_frame()
        self._create_files_frame()
        self._create_progress_frame()
        self._create_console_frame()
        
        # Load keywords
        try:
            self.match_keywords = core.load_keywords("match.txt")
            self.ignore_keywords = core.load_keywords("ignore.txt")
        except Exception as e:
            self._log_error(f"Error loading keywords: {str(e)}")
        
        # Log initial message
        self._log_info("Chương trình đã sẵn sàng")

    # UI Creation Methods
    def _create_instruction_frame(self) -> None:
        """Create instruction frame with step-by-step guide and supported file types."""
        # Create a container frame for instruction and supported files
        container = ttk.Frame(self.left_pane)
        container.pack(fill=tk.X, padx=10, pady=5)
        
        # Create instruction frame
        instruction_frame = ttk.LabelFrame(
            container,
            text=c.INSTRUCTION_FRAME_TEXT,
            padding="10"
        )
        instruction_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Add instruction text with proper formatting
        instruction_text = tk.Text(
            instruction_frame,
            wrap=tk.WORD,
            font=('TkDefaultFont', 9),
            relief=tk.FLAT,
            background=self.root.cget('bg')
        )
        instruction_text.pack(fill=tk.BOTH, expand=True, padx=5)
        instruction_text.insert('1.0', c.INSTRUCTION_TEXT)
        line_count = instruction_text.index('end-1c').split('.')[0]  # Đếm số dòng thực tế
        instruction_text.configure(height=int(line_count), state='disabled')  

        # Create supported files frame on the right
        self.supported_frame = ttk.LabelFrame(
            container,
            text=c.SUPPORTED_FILES_TEXT,
            padding="10"
        )
        self.supported_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))
        
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

    def _create_progress_frame(self) -> None:
        """Create progress frame for displaying file loading progress."""
        self.progress_frame = ttk.Frame(self.left_pane)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)

    def _create_console_frame(self) -> None:
        """Create console frame for logs."""
        console_frame = ttk.LabelFrame(
            self.right_pane,
            text=c.CONSOLE_TEXT,
            padding="5"
        )
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text widget for logs
        self.console = tk.Text(
            console_frame,
            wrap=tk.WORD,
            height=10,
            font=('Consolas', 9),
            background='white'
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            console_frame,
            orient=tk.VERTICAL,
            command=self.console.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.configure(yscrollcommand=scrollbar.set)
        
        # Make read-only
        self.console.configure(state='disabled')
        
        
    # Logging Methods
    def _log(self, level: str, message: str) -> None:
        """Log a message to the console."""
        timestamp = datetime.now().strftime(c.LOG_TIME_FORMAT)
        log_message = f"{timestamp} {level} {message}\n"
        
        self.console.configure(state='normal')
        self.console.insert(tk.END, log_message)
        self.console.see(tk.END)
        self.console.configure(state='disabled')
        
    def _log_info(self, message: str) -> None:
        """Log an info message."""
        self._log(c.LOG_INFO, message)
        
    def _log_error(self, message: str) -> None:
        """Log an error message."""
        self._log(c.LOG_ERROR, message)
        
    def _create_directory_frame(self) -> None:
        """Create frame for directory selection and action buttons."""
        self.dir_frame = ttk.LabelFrame(
            self.left_pane,
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
        
        # Add Apply button
        self.apply_btn = ttk.Button(
            self.dir_frame,
            text=c.APPLY_BTN,
            command=self.apply_changes
        )
        self.apply_btn.pack(side=tk.RIGHT, padx=5)
        
    def _create_files_frame(self) -> None:
        """Create frame with treeview for displaying original and new filenames."""
        self.files_frame = ttk.LabelFrame(
            self.left_pane,
            text=c.FILES_FRAME_TEXT,
            padding="10"
        )
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.files_frame,
            columns=(
                c.ORIGINAL_NAME_COL,
                c.NEW_NAME_COL
            ),
            show="headings"
        )
        
        # Configure columns
        self.tree.heading(c.ORIGINAL_NAME_COL, text=c.ORIGINAL_NAME_COL)
        self.tree.heading(c.NEW_NAME_COL, text=c.NEW_NAME_COL)
        
        self.tree.column(c.ORIGINAL_NAME_COL, width=c.NAME_COL_WIDTH)
        self.tree.column(c.NEW_NAME_COL, width=c.NAME_COL_WIDTH)
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(
            self.files_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        
        h_scrollbar = ttk.Scrollbar(
            self.files_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        
        # Pack scrollbars
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Pack the tree between the scrollbars
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.tree.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
    # File Operation Methods
    def load_files(self) -> None:
        """Load files from selected directory."""
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.current_directory = directory
            self.dir_label.config(text=directory)
            self.files = fo.get_files_in_directory(
                directory,
                extensions=['.doc', '.docx'],
                exclude_patterns=['★'],
                limit=20
            )
            
            if not self.files:
                self._log_info(f"Không tìm thấy tập tin hỗ trợ trong thư mục: {directory}")
                return
                
            self.used_names.clear()
            
            # Show progress with file limit info
            self._log_info(f"Bắt đầu tải {len(self.files)} tập tin (giới hạn 20 tập tin .doc/.docx) từ: {directory}")
            self.progress_bar = ttk.Progressbar(
                self.progress_frame,
                mode='determinate',
                maximum=len(self.files)
            )
            self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Start loading files
            self.tree.delete(*self.tree.get_children())
            self._load_next_file(0)
            
    def _load_next_file(self, index: int) -> None:
        """Load next file."""
        if index >= len(self.files):
            # Done loading
            self._log_info("✓ Đã tải xong tất cả tập tin")
            self.progress_bar.pack_forget()
            return
            
        file = self.files[index]
        file_path = os.path.join(self.current_directory, file)
        
        # Update progress bar
        self.progress_bar["value"] = index + 1
        self._log_info(f"⏳ ({index + 1}/{len(self.files)}) Đang tải: {file}")
        result = core.rename_file_with_rules(
            file_path,
            self.match_keywords,
            self.ignore_keywords,
            line_limit=10,
            length_limit=200
        )
        new_name = os.path.basename(result) if result else file
        self.tree.insert("", tk.END, values=(file, new_name))
        self.root.update_idletasks()
        self.root.after(10, self._load_next_file, index + 1)
            
            
    # Event Handler Methods
    def apply_changes(self, rename_in_place: bool = True) -> None:
        """Apply the rename changes with confirmation.
        
        Args:
            rename_in_place: If True, rename files in current directory.
                           If False, create copies in a new directory.
        """
        if not self._validate_directory():
            self._log_error(c.WARNING_SELECT_DIR)
            return
        
        action_msg = "đổi tên" if rename_in_place else "sao chép"
        if not messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc chắn muốn {action_msg} các tập tin đã chọn không?",
            icon='warning'
        ):
            return
        
        try:
            # Get all files to rename
            files_to_rename = [
                (self.tree.item(item)["values"][0], self.tree.item(item)["values"][1])
                for item in self.tree.get_children()
            ]
            
            success_count = 0
            for old_name, new_name in files_to_rename:
                if old_name == new_name:
                    continue
                
                old_path = os.path.join(self.current_directory, old_name)
                
                if rename_in_place:
                    new_path = os.path.join(self.current_directory, new_name)
                    # Handle duplicate filenames
                    new_path = core.get_unique_filename(new_path)
                    final_name = os.path.basename(new_path)
                    # Rename file in place
                    os.rename(old_path, new_path)
                else:
                    # Create renamed directory for copies
                    new_dir = os.path.join(self.current_directory, c.RENAMED_FILES_DIR)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    new_path = os.path.join(new_dir, new_name)
                    # Handle duplicate filenames
                    new_path = core.get_unique_filename(new_path)
                    final_name = os.path.basename(new_path)
                    # Copy file with new name
                    shutil.copy2(old_path, new_path)
                
                success_count += 1
                operation = "✓ Đổi tên" if rename_in_place else "✓ Sao chép"
                self._log_info(f"{operation}: {old_name} → {final_name}")
            
            if success_count > 0:
                if rename_in_place:
                    self._log_info(f"Đã đổi tên {success_count} tập tin thành công")
                else:
                    self._log_info(c.SUCCESS_MESSAGE.format(new_dir))
            else:
                self._log_info(c.NO_CHANGES_MESSAGE)
                
        except Exception as e:
            self._log_error(c.ERROR_MESSAGE.format(str(e)))
            
    def _validate_directory(self) -> bool:
        """Validate if directory is selected."""
        if not self.current_directory:
            return False
        return True
        