import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext, colorchooser

# --- Define Roblox IxpSettings path dynamically ---
home_dir = Path.home()
roblox_dir = home_dir / "AppData" / "Local" / "Roblox" / "ClientSettings"
filename = "IxpSettings.json"
roblox_path = roblox_dir / filename

# --- Themes ---
themes = {
    "Light": {
        "bg": "#f0f0f0", "fg": "#000000",
        "text_bg": "#ffffff", "text_fg": "#000000",
        "button_bg": "#e0e0e0", "button_fg": "#000000",
    },
    "Dark": {
        "bg": "#212326", "fg": "#ffffff",
        "text_bg": "#2c2f33", "text_fg": "#f8f8f8",
        "button_bg": "#444444", "button_fg": "#ffffff",
    },
    "Blue": {
        "bg": "#dce9f9", "fg": "#000033",
        "text_bg": "#eaf2fc", "text_fg": "#001144",
        "button_bg": "#a7c7f2", "button_fg": "#000033",
    },
    "Green": {
        "bg": "#e5f5e0", "fg": "#003300",
        "text_bg": "#f0fff0", "text_fg": "#003300",
        "button_bg": "#a7e9af", "button_fg": "#003300",
    }
}
current_theme = "Dark"

# --- File management functions ---
def ensure_file_exists():
    """Ensure Roblox IxpSettings.json exists and is valid."""
    try:
        roblox_dir.mkdir(parents=True, exist_ok=True)
        if not roblox_path.exists():
            with open(roblox_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
            messagebox.showinfo("File Created", "IxpSettings.json was missing and has been created.")
        else:
            # Validate JSON structure
            with open(roblox_path, "r", encoding="utf-8") as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    messagebox.showwarning(
                        "Invalid JSON",
                        "IxpSettings.json was corrupted — replaced with empty JSON."
                    )
                    with open(roblox_path, "w", encoding="utf-8") as f2:
                        json.dump({}, f2, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to prepare file: {e}")

def load_file_content():
    """Load IxpSettings.json into editor."""
    ensure_file_exists()
    try:
        with open(roblox_path, "r", encoding="utf-8") as f:
            content = f.read()
        text_widget.delete('1.0', tk.END)
        text_widget.insert('1.0', content)
        messagebox.showinfo("Loaded", f"Loaded content from {roblox_path.name}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file: {e}")

def save_file_content():
    """Save editor content to IxpSettings.json (valid JSON only)."""
    ensure_file_exists()
    content = text_widget.get('1.0', tk.END).strip()
    if not content:
        messagebox.showwarning("Empty File", "Cannot save an empty file.")
        return
    try:
        parsed = json.loads(content)
        with open(roblox_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4)
        messagebox.showinfo("Saved", f"Changes saved to {roblox_path.name} successfully!")
    except json.JSONDecodeError as e:
        messagebox.showerror("Invalid JSON", f"File content is not valid JSON:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")

def toggle_read_only():
    """Toggle read-only attribute of IxpSettings.json."""
    ensure_file_exists()
    try:
        writable = os.access(roblox_path, os.W_OK)
        os.chmod(roblox_path, 0o444 if writable else 0o666)
        state = "READ-ONLY" if writable else "WRITABLE"
        messagebox.showinfo("Read-Only", f"IxpSettings.json set to {state}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to toggle read-only: {e}")

# --- Theme functions ---
def apply_theme(theme_name, custom_data=None):
    """Apply selected theme or custom colors."""
    global current_theme
    current_theme = theme_name
    theme = custom_data if custom_data else themes[theme_name]

    root.config(bg=theme["bg"])
    top_frame.config(bg=theme["bg"])
    bottom_frame.config(bg=theme["bg"])
    edit_frame.config(bg=theme["bg"])

    text_widget.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
    for btn in (toggle_button, load_button, save_button):
        btn.config(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["bg"])

def open_custom_theme_editor():
    """Popup to define and apply a custom color theme."""
    editor = tk.Toplevel(root)
    editor.title("Custom Theme Editor")

    labels = ["Background", "Foreground", "Text BG", "Text FG", "Button BG", "Button FG"]
    keys = ["bg", "fg", "text_bg", "text_fg", "button_bg", "button_fg"]
    entries = {}

    def pick_color(key):
        color = colorchooser.askcolor()[1]
        if color:
            entries[key].delete(0, tk.END)
            entries[key].insert(0, color)

    for i, (label, key) in enumerate(zip(labels, keys)):
        tk.Label(editor, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(editor, width=10)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[key] = entry
        tk.Button(editor, text="Pick", command=lambda k=key: pick_color(k)).grid(row=i, column=2, padx=5, pady=5)

    def apply_custom():
        custom = {k: entries[k].get() or "#ffffff" for k in keys}
        apply_theme("Custom", custom)
        editor.destroy()

    tk.Button(editor, text="Apply Custom Theme", command=apply_custom).grid(row=len(labels), columnspan=3, pady=10)

# --- GUI setup ---
root = tk.Tk()
root.title("Roblox IxpSettings Manager")
root.geometry("780x560")

# Menu bar
menubar = tk.Menu(root)
theme_menu = tk.Menu(menubar, tearoff=0)
for t in themes.keys():
    theme_menu.add_command(label=t, command=lambda name=t: apply_theme(name))
theme_menu.add_separator()
theme_menu.add_command(label="Custom Theme...", command=open_custom_theme_editor)
menubar.add_cascade(label="Themes", menu=theme_menu)
root.config(menu=menubar)

# --- Top Frame ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

toggle_button = tk.Button(top_frame, text="Toggle Read-Only", command=toggle_read_only)
toggle_button.pack(side=tk.LEFT, padx=10)

# --- Text Editor ---
edit_frame = tk.Frame(root)
edit_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

text_widget = scrolledtext.ScrolledText(edit_frame, wrap=tk.WORD, font=("Consolas", 10))
text_widget.pack(fill=tk.BOTH, expand=True)

# --- Bottom Frame ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

load_button = tk.Button(bottom_frame, text="Load File", command=load_file_content)
load_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(bottom_frame, text="Save Changes", command=save_file_content)
save_button.pack(side=tk.LEFT, padx=10)

# Apply initial theme and load file
apply_theme(current_theme)
ensure_file_exists()
load_file_content()

root.mainloop()
