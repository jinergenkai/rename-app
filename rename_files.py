import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import shutil

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer Tool")
        self.root.geometry("800x600")
        
        # Store current directory
        self.current_directory = None
        
        # Directory frame
        self.dir_frame = ttk.LabelFrame(root, text="Selected Directory", padding="10")
        self.dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.dir_label = ttk.Label(self.dir_frame, text="No directory selected")
        self.dir_label.pack(fill=tk.X)
        
        # File list
        self.files_frame = ttk.LabelFrame(root, text="Files to Rename", padding="10")
        self.files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create treeview
        self.tree = ttk.Treeview(self.files_frame, columns=("Original Name", "New Name"), show="headings")
        self.tree.heading("Original Name", text="Original Name")
        self.tree.heading("New Name", text="New Name")
        self.tree.column("Original Name", width=300)
        self.tree.column("New Name", width=300)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.files_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(root, padding="10")
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Load files button
        self.load_btn = ttk.Button(self.buttons_frame, text="Load Directory", command=self.load_files)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Rename pattern frame
        self.pattern_frame = ttk.LabelFrame(root, text="Rename Pattern", padding="10")
        self.pattern_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Prefix entry
        ttk.Label(self.pattern_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_var = tk.StringVar()
        self.prefix_entry = ttk.Entry(self.pattern_frame, textvariable=self.prefix_var)
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        
        # Suffix entry
        ttk.Label(self.pattern_frame, text="Suffix:").pack(side=tk.LEFT, padx=5)
        self.suffix_var = tk.StringVar()
        self.suffix_entry = ttk.Entry(self.pattern_frame, textvariable=self.suffix_var)
        self.suffix_entry.pack(side=tk.LEFT, padx=5)
        
        # Preview button
        self.preview_btn = ttk.Button(self.pattern_frame, text="Preview Changes", command=self.preview_changes)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        # Apply button
        self.apply_btn = ttk.Button(self.pattern_frame, text="Apply Changes", command=self.apply_changes)
        self.apply_btn.pack(side=tk.LEFT, padx=5)
        
        self.files = []
        
    def load_files(self):
        directory = filedialog.askdirectory(initialdir=os.getcwd())
        if directory:
            self.current_directory = directory
            self.dir_label.config(text=directory)
            self.files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            self.tree.delete(*self.tree.get_children())
            for file in self.files:
                self.tree.insert("", tk.END, values=(file, file))
                
    def preview_changes(self):
        if not self.current_directory:
            messagebox.showwarning("Warning", "Please select a directory first!")
            return
            
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        
        self.tree.delete(*self.tree.get_children())
        for file in self.files:
            name, ext = os.path.splitext(file)
            new_name = f"{prefix}{name}{suffix}{ext}"
            self.tree.insert("", tk.END, values=(file, new_name))
            
    def apply_changes(self):
        if not self.current_directory:
            messagebox.showwarning("Warning", "Please select a directory first!")
            return
            
        try:
            # Create new directory for renamed files
            new_dir = os.path.join(self.current_directory, "renamed_files")
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            
            changes_made = False
            for item in self.tree.get_children():
                old_name, new_name = self.tree.item(item)["values"]
                if old_name != new_name:
                    old_path = os.path.join(self.current_directory, old_name)
                    new_path = os.path.join(new_dir, new_name)
                    
                    # Copy file with new name to new directory
                    shutil.copy2(old_path, new_path)
                    changes_made = True
            
            if changes_made:
                messagebox.showinfo("Success", f"Files have been copied and renamed in:\n{new_dir}")
            else:
                messagebox.showinfo("Info", "No changes to apply.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()