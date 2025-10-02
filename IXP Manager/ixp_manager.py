import shutil
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Define paths dynamically using pathlib for cross-platform compatibility ---
home_dir = Path.home()
roblox_dir = home_dir / "AppData" / "Local" / "Roblox" / "ClientSettings"
fishstrap_dir = home_dir / "AppData" / "Local" / "Fishstrap" / "Modifications"
filename = "IxpSettings.json"

roblox_path = roblox_dir / filename
fishstrap_path = fishstrap_dir / filename

# --- GUI functions ---
def get_current_file_path():
    """Checks the location of the file and returns the current Path object."""
    if fishstrap_path.exists():
        return fishstrap_path
    elif roblox_path.exists():
        return roblox_path
    return None

def load_file_content():
    """Loads the content of the file into the text editor."""
    current_path = get_current_file_path()
    text_widget.delete('1.0', tk.END)  # Clear current text
    if current_path:
        try:
            with open(current_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert('1.0', content)  # Insert file content
            messagebox.showinfo("Loaded", f"Loaded content from {current_path.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")
    else:
        messagebox.showwarning("File Not Found", "The IxpSettings.json file was not found in either location.")

def save_file_content():
    """Saves the content from the text editor back to the current file."""
    current_path = get_current_file_path()
    if current_path:
        try:
            content = text_widget.get('1.0', tk.END)  # Get all text from widget
            with open(current_path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Changes saved to {current_path.name} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        messagebox.showwarning("File Not Found", "No file is currently active to save changes to.")

def move_file():
    """Moves the IxpSettings.json file from Roblox to Fishstrap."""
    fishstrap_dir.mkdir(parents=True, exist_ok=True)
    
    if roblox_path.exists():
        try:
            shutil.move(roblox_path, fishstrap_path)
            messagebox.showinfo("Success", "IxpSettings.json moved to Fishstrap successfully!")
            load_file_content()  # Reload text field with content from new location
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move file: {e}")
    else:
        messagebox.showwarning("File Not Found", "File not found in the Roblox folder.")

def restore_file():
    """Restores the IxpSettings.json file from Fishstrap back to Roblox."""
    if fishstrap_path.exists():
        try:
            shutil.move(fishstrap_path, roblox_path)
            messagebox.showinfo("Success", "IxpSettings.json restored to Roblox successfully!")
            load_file_content()  # Reload text field with content from new location
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore file: {e}")
    else:
        messagebox.showwarning("File Not Found", "File not found in the Fishstrap folder.")

# --- GUI setup ---
root = tk.Tk()
root.title("IxpSettings Manager and Editor")
root.geometry("700x500")

# --- Top Frame for file manipulation buttons ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

move_button = tk.Button(top_frame, text="Move to Fishstrap", command=move_file)
move_button.pack(side=tk.LEFT, padx=10)

restore_button = tk.Button(top_frame, text="Restore to Roblox", command=restore_file)
restore_button.pack(side=tk.LEFT, padx=10)

# --- Text Editing Frame ---
edit_frame = tk.Frame(root)
edit_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# ScrolledText widget for multi-line editing
text_widget = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, width=80, height=20, font=("Courier New", 10))
text_widget.pack(fill=tk.BOTH, expand=True)

# --- Bottom Frame for text editing buttons ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

load_button = tk.Button(bottom_frame, text="Load File", command=load_file_content)
load_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(bottom_frame, text="Save Changes", command=save_file_content)
save_button.pack(side=tk.LEFT, padx=10)

# Initial load of file content
load_file_content()

# Start the GUI event loop
root.mainloop()