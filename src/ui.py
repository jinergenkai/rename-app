"""GUI components and event handlers."""

import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from typing import List, Optional, Callable, Dict, Set

from . import constants as c
from . import file_operations as fo
from . import ai_operations as ai

class APIKeyDialog(simpledialog.Dialog):
    """Dialog for entering API key."""
    
    def body(self, master):
        ttk.Label(master, text=c.API_KEY_PROMPT).grid(row=0, column=0, padx=5, pady=5)
        self.entry = ttk.Entry(master, width=50, show="*")
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        return self.entry
        
    def apply(self):
        self.result = self.entry.get()

class FileRenamerUI:
    def __init__(self, root: tk.Tk):
        """Initialize the UI components."""
        self.root = root
        self.root.title(c.WINDOW_TITLE)
        # self.root.geometry(c.WINDOW_SIZE)
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
        
        # Initialize with content pattern
        self.pattern = tk.StringVar(value=c.PATTERN_CONTENT)
        
        # Store file previews and AI summaries
        self.preview_cache: Dict[str, str] = {}
        self.ai_summaries: Dict[str, str] = {}
        
        # Track used filenames
        self.used_names: Set[str] = set()
        
        # Create progress frame first
        self._create_progress_frame()
        
        # Create instruction frame at the top
        self._create_instruction_frame()
        
        # Create UI components in left pane
        self._create_directory_frame()
        self._create_options_frame()
        self._create_files_frame()
        self._create_buttons_frame()
        
        # Create console in right pane
        self._create_console_frame()
        
        # Hide prefix/suffix frame by default since we're using content pattern
        self.prefix_suffix_frame.pack_forget()
        
        # Log initial message
        self._log_info("Chương trình đã sẵn sàng")

    def _create_instruction_frame(self) -> None:
        """Create instruction frame with step-by-step guide."""
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
        """Create progress frame."""
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
        """Create the directory selection frame."""
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
        
        # Add API Key button
        self.api_btn = ttk.Button(
            self.dir_frame,
            text=c.API_KEY_BUTTON,
            command=self._set_api_key
        )
        self.api_btn.pack(side=tk.RIGHT, padx=5)
        
    def _set_api_key(self) -> None:
        """Show dialog to set API key."""
        dialog = APIKeyDialog(self.root)
        if dialog.result:
            try:
                ai.save_api_key(dialog.result)
                self._log_info(c.API_KEY_SAVED)
            except Exception as e:
                self._log_error(str(e))
        
    def _create_options_frame(self) -> None:
        """Create frame for preview options and supported files."""
        options_frame = ttk.Frame(self.left_pane)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Preview options on the left
        preview_frame = ttk.LabelFrame(
            options_frame,
            text=c.PREVIEW_OPTIONS_TEXT,
            padding="10"
        )
        preview_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        
        # Pattern selection
        pattern_frame = ttk.Frame(preview_frame)
        pattern_frame.pack(side=tk.LEFT, padx=20)
        
        for pattern in c.PATTERN_OPTIONS:
            ttk.Radiobutton(
                pattern_frame,
                text=pattern,
                value=pattern,
                variable=self.pattern,
                command=self._on_pattern_change
            ).pack(side=tk.LEFT, padx=10)
        
        # Prefix/Suffix frame
        self.prefix_suffix_frame = ttk.Frame(preview_frame)
        self.prefix_suffix_frame.pack(side=tk.LEFT, padx=20)
        
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
        
        # Hide prefix/suffix frame by default
        self.prefix_suffix_frame.pack_forget()
        
        # Supported files frame is now created in _create_instruction_frame
        
    def _create_buttons_frame(self) -> None:
        """Create frame for action buttons."""
        buttons_frame = ttk.Frame(self.left_pane)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Preview and Apply buttons on the left
        self.preview_btn = ttk.Button(
            buttons_frame,
            text=c.PREVIEW_BTN,
            command=self.preview_changes
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.apply_btn = ttk.Button(
            buttons_frame,
            text=c.APPLY_BTN,
            command=self.apply_changes
        )
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        
    def _create_files_frame(self) -> None:
        """Create the files list frame with treeview."""
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
                c.NEW_NAME_COL,
                c.PREVIEW_COL,
                c.AI_SUMMARY_COL
            ),
            show="headings"
        )
        
        # Configure columns
        self.tree.heading(c.ORIGINAL_NAME_COL, text=c.ORIGINAL_NAME_COL)
        self.tree.heading(c.NEW_NAME_COL, text=c.NEW_NAME_COL)
        self.tree.heading(c.PREVIEW_COL, text=c.PREVIEW_COL)
        self.tree.heading(c.AI_SUMMARY_COL, text=c.AI_SUMMARY_COL)
        
        self.tree.column(c.ORIGINAL_NAME_COL, width=c.NAME_COL_WIDTH)
        self.tree.column(c.NEW_NAME_COL, width=c.NAME_COL_WIDTH)
        self.tree.column(c.PREVIEW_COL, width=c.PREVIEW_COL_WIDTH)
        self.tree.column(c.AI_SUMMARY_COL, width=c.AI_SUMMARY_COL_WIDTH)
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
        
    def load_files(self) -> None:
        """Load files from selected directory."""
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.current_directory = directory
            self.dir_label.config(text=directory)
            self.files = fo.get_files_in_directory(directory)
            
            if not self.files:
                self._log_info(f"Không tìm thấy tập tin hỗ trợ trong thư mục: {directory}")
                return
                
            self.preview_cache.clear()
            self.ai_summaries.clear()
            self.used_names.clear()
            
            # Show progress
            self._log_info(f"Bắt đầu tải {len(self.files)} tập tin từ: {directory}")
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
        """Load next file and its preview."""
        if index >= len(self.files):
            # Done loading
            self._log_info("✓ Đã tải xong tất cả tập tin")
            self.progress_bar.pack_forget()
            return
            
        file = self.files[index]
        file_path = os.path.join(self.current_directory, file)
        
        # Update progress
        progress = (index + 1) / len(self.files) * 100
        self.progress_bar["value"] = index + 1
        self._log_info(f"⏳ ({index + 1}/{len(self.files)}) Đang tải: {file}")
        # Get preview and add to tree
        try:
            preview = fo.get_file_preview(file_path)
            if "Không thể đọc" in preview or "Cần cài đặt" in preview:
                self._log_error(f"⚠ {file}: {preview}")
            else:
                self._log_info(f"✓ Đã tải: {file}")
        except Exception as e:
            preview = str(e)
            self._log_error(f"⚠ {file}: {preview}")
            
        self.preview_cache[file] = preview
        self.tree.insert("", tk.END, values=(file, file, preview, ""))
        
        # Update UI immediately
        self.root.update_idletasks()
        
        # Schedule next file load
        self.root.after(10, self._load_next_file, index + 1)
            
    def _refresh_previews(self) -> None:
        """Refresh all file previews with new line count."""
        if not self.current_directory or not self.files:
            return
            
        self.preview_cache.clear()
        self.used_names.clear()
        self._update_tree_view(self.files)
    
    def _on_pattern_change(self) -> None:
        """Handle pattern selection change."""
        pattern = self.pattern.get()
        
        # Show message and reset pattern if AI Summary is selected
        if pattern == c.PATTERN_AI:
            messagebox.showinfo("Thông báo", "Tính năng AI Tóm tắt hiện đang bị tắt.")
            self.pattern.set(c.PATTERN_CONTENT)
            return
            
        # Show/hide prefix/suffix inputs
        if pattern == c.PATTERN_PREFIX_SUFFIX:
            self.prefix_suffix_frame.pack(side=tk.LEFT, padx=20)
        else:
            self.prefix_suffix_frame.pack_forget()
            
    def preview_changes(self) -> None:
        """Preview filename changes."""
        if not self._validate_directory():
            self._log_error(c.WARNING_SELECT_DIR)
            return
            
        pattern = self.pattern.get()
        if pattern == c.PATTERN_AI:
            # Check for API key
            if not ai.load_api_key():
                self._log_error(c.API_KEY_REQUIRED)
                return

        self._log_info(f"Xem trước thay đổi với kiểu: {pattern}")
        
        # Clear used names for new preview
        self.used_names.clear()
        self.ai_summaries.clear()
        self._update_tree_view(self.files)
            
    def apply_changes(self) -> None:
        """Apply the rename changes with confirmation."""
        if not self._validate_directory():
            self._log_error(c.WARNING_SELECT_DIR)
            return
            
        if not messagebox.askyesno(
            "Xác nhận",
            c.CONFIRM_APPLY_DETAIL,
            icon='warning'
        ):
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
        
    def _update_tree_view(
        self,
        files: List[str],
        new_name_func: Optional[Callable[[str], str]] = None
    ) -> None:
        """Update the tree view with files."""
        self.tree.delete(*self.tree.get_children())
        pattern = self.pattern.get()
        
        # Show progress for AI processing
        if pattern == c.PATTERN_AI:
            self.progress_bar = ttk.Progressbar(
                self.progress_frame,
                mode='determinate',
                maximum=len(files)
            )
            self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            self._log_info(f"Bắt đầu xử lý AI cho {len(files)} tập tin")
        
        for i, file in enumerate(files):
            preview = self.preview_cache.get(file, "Loading...")
            ai_summary = self.ai_summaries.get(file, "")
            
            try:
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
                elif pattern == c.PATTERN_AI:
                    self._log_info(f"⏳ ({i + 1}/{len(files)}) Đang xử lý AI: {file}")
                    self.progress_bar["value"] = i + 1
                    
                    new_name = fo.create_new_filename(
                        file,
                        pattern,
                        content=preview,
                        used_names=self.used_names,
                        ai_summaries=self.ai_summaries
                    )
                    ai_summary = self.ai_summaries.get(file, "")
                    self._log_info(f"✓ Đã xử lý AI: {file}")
                else:
                    new_name = file
                    
                if new_name != file:
                    self._log_info(f"→ {file} → {new_name}")
                    
            except Exception as e:
                new_name = file
                self._log_error(f"⚠ {file}: {str(e)}")
                
            self.tree.insert("", tk.END, values=(file, new_name, preview, ai_summary))
            
            # Update UI immediately
            self.root.update_idletasks()
        
        # Remove progress bar after AI processing
        if pattern == c.PATTERN_AI:
            self.progress_bar.pack_forget()
            self._log_info("✓ Đã hoàn thành xử lý AI")