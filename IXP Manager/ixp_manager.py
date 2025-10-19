import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

# --- Define Roblox IxpSettings path ---
home_dir = Path.home()
roblox_dir = home_dir / "AppData" / "Local" / "Roblox" / "ClientSettings"
ixp_path = roblox_dir / "IxpSettings.json"

# --- Create file if missing or invalid ---
def ensure_ixp_file():
    try:
        roblox_dir.mkdir(parents=True, exist_ok=True)
        if not ixp_path.exists():
            with open(ixp_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
        else:
            with open(ixp_path, "r", encoding="utf-8") as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    with open(ixp_path, "w", encoding="utf-8") as f2:
                        json.dump({}, f2, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Could not prepare IxpSettings.json:\n{e}")

# --- Core functions ---
def load_ixp():
    ensure_ixp_file()
    try:
        with open(ixp_path, "r", encoding="utf-8") as f:
            text_box.delete("1.0", tk.END)
            text_box.insert("1.0", f.read())
        messagebox.showinfo("Loaded", "Loaded IxpSettings.json successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")

def save_ixp():
    ensure_ixp_file()
    content = text_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Empty", "Cannot save an empty file.")
        return
    try:
        json.loads(content)  # validate
        with open(ixp_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", "Saved IxpSettings.json successfully.")
    except json.JSONDecodeError as e:
        messagebox.showerror("Invalid JSON", f"Invalid JSON:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")

def toggle_readonly():
    ensure_ixp_file()
    try:
        if os.access(ixp_path, os.W_OK):
            os.chmod(ixp_path, 0o444)
            messagebox.showinfo("Read-Only", "IxpSettings.json set to READ-ONLY.")
        else:
            os.chmod(ixp_path, 0o666)
            messagebox.showinfo("Writable", "IxpSettings.json set to WRITABLE.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to toggle read-only:\n{e}")

# --- UI setup ---
root = tk.Tk()
root.title("Roblox IxpSettings Manager")
root.geometry("700x500")
root.configure(bg="#1e1f22")

# --- Styles ---
BG = "#1e1f22"
FG = "#f8f8f8"
BTN_BG = "#2f3136"
BTN_FG = "#ffffff"
BTN_ACTIVE = "#3a3c42"
FONT = ("Consolas", 11)

# --- Title ---
title_label = tk.Label(
    root,
    text="Roblox IxpSettings Manager",
    font=("Segoe UI", 14, "bold"),
    fg=FG,
    bg=BG
)
title_label.pack(pady=(15, 5))

# --- Text Editor ---
text_box = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    bg="#2b2d31",
    fg=FG,
    insertbackground=FG,
    font=FONT,
    height=18,
    width=80,
    borderwidth=0,
    relief="flat",
)
text_box.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# --- Button Frame ---
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

def make_btn(text, cmd):
    return tk.Button(
        btn_frame,
        text=text,
        command=cmd,
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground=BTN_ACTIVE,
        activeforeground=FG,
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=6,
        cursor="hand2",
    )

load_btn = make_btn("📂 Load from Ixp", load_ixp)
save_btn = make_btn("💾 Save to Ixp", save_ixp)
ro_btn = make_btn("🔒 Toggle Read-Only", toggle_readonly)

load_btn.grid(row=0, column=0, padx=8)
save_btn.grid(row=0, column=1, padx=8)
ro_btn.grid(row=0, column=2, padx=8)

# --- Initialize ---
ensure_ixp_file()
load_ixp()

# --- Run ---
root.mainloop()
