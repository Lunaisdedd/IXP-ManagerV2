import shutil
import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

# --- Define paths dynamically ---
home_dir = Path.home()
roblox_dir = home_dir / "AppData" / "Local" / "Roblox" / "ClientSettings"
fishstrap_dir = home_dir / "AppData" / "Local" / "Fishstrap" / "Modifications" / "ClientSettings"
filename = "IxpSettings.json"

roblox_path = roblox_dir / filename
fishstrap_path = fishstrap_dir / filename

# --- File management functions ---
def get_current_file_path():
    if fishstrap_path.exists():
        return fishstrap_path
    elif roblox_path.exists():
        return roblox_path
    return None

def load_file_content():
    """Loads IxpSettings.json into editor."""
    current_path = get_current_file_path()
    text_widget.delete('1.0', tk.END)
    if current_path:
        try:
            with open(current_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert('1.0', content)
            messagebox.showinfo("Loaded", f"Loaded content from {current_path.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")
    else:
        messagebox.showwarning("File Not Found", f"{filename} not found in either location.")

def save_file_content():
    """Saves editor content to active IxpSettings.json."""
    current_path = get_current_file_path()
    if current_path:
        try:
            content = text_widget.get('1.0', tk.END)
            with open(current_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Changes saved to {current_path.name} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        messagebox.showwarning("File Not Found", "No file is active to save changes to.")

def move_file():
    """Moves IxpSettings.json from Roblox to Fishstrap."""
    fishstrap_dir.mkdir(parents=True, exist_ok=True)
    if roblox_path.exists():
        try:
            os.chmod(roblox_path, 0o666)  # remove read-only if set
            shutil.move(roblox_path, fishstrap_path)
            messagebox.showinfo("Success", "IxpSettings.json moved to Fishstrap successfully!")
            load_file_content()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move file: {e}")
    else:
        messagebox.showwarning("File Not Found", "File not found in Roblox folder.")

def restore_file():
    """Restores IxpSettings.json back to Roblox (keeps current read-only state)."""
    if fishstrap_path.exists():
        try:
            shutil.move(fishstrap_path, roblox_path)
            messagebox.showinfo("Success", "IxpSettings.json restored to Roblox successfully!")
            load_file_content()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore file: {e}")
    else:
        messagebox.showwarning("File Not Found", "File not found in Fishstrap folder.")

def toggle_read_only():
    """Toggle read-only attribute on Roblox IxpSettings.json."""
    if roblox_path.exists():
        try:
            if os.access(roblox_path, os.W_OK):  # currently writable
                os.chmod(roblox_path, 0o444)     # make read-only
                messagebox.showinfo("Read-Only", "IxpSettings.json set to READ-ONLY.")
            else:
                os.chmod(roblox_path, 0o666)     # make writable
                messagebox.showinfo("Read-Only", "IxpSettings.json set to WRITABLE.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle read-only: {e}")
    else:
        messagebox.showwarning("File Not Found", "Roblox IxpSettings.json not found.")

def import_json_file():
    """Let user choose a JSON file and load it into editor."""
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            formatted = json.dumps(data, indent=4)
            text_widget.delete('1.0', tk.END)
            text_widget.insert('1.0', formatted)
            messagebox.showinfo("Imported", f"Imported {os.path.basename(file_path)} into editor.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load JSON file: {e}")

# --- GUI setup ---
root = tk.Tk()
root.title("IxpSettings Manager and Editor")
root.geometry("750x550")

# --- Top Frame for file manipulation buttons ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

move_button = tk.Button(top_frame, text="Move to Fishstrap", command=move_file)
move_button.pack(side=tk.LEFT, padx=10)

restore_button = tk.Button(top_frame, text="Restore to Roblox", command=restore_file)
restore_button.pack(side=tk.LEFT, padx=10)

toggle_button = tk.Button(top_frame, text="Toggle Read-Only", command=toggle_read_only)
toggle_button.pack(side=tk.LEFT, padx=10)

import_button = tk.Button(top_frame, text="Import JSON", command=import_json_file)
import_button.pack(side=tk.LEFT, padx=10)

# --- Text Editing Frame ---
edit_frame = tk.Frame(root)
edit_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

text_widget = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, width=85, height=22, font=("Courier New", 10))
text_widget.pack(fill=tk.BOTH, expand=True)

# --- Bottom Frame ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

load_button = tk.Button(bottom_frame, text="Load File", command=load_file_content)
load_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(bottom_frame, text="Save Changes", command=save_file_content)
save_button.pack(side=tk.LEFT, padx=10)

# Initial load
load_file_content()

# Start GUI
root.mainloop()
