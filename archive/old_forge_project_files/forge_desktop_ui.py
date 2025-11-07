#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ 2025 Robert Demotto Jr
FORGE DESKTOP UI — Cinematic Integration Edition
─────────────────────────────────────────────────────────────
✅ Tkinter control panel for Forge system
✅ Launch system, cinematic, and analysis from GUI
✅ Live console output mirroring
─────────────────────────────────────────────────────────────
"""

import os, subprocess, threading, tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

ROOT_DIR = os.getcwd()
PROJECT_DIR = os.path.join(ROOT_DIR, "forge_project")
FORGE_LAUNCH = os.path.join(PROJECT_DIR, "forge_system_launch.py")
CINEMATIC = os.path.join(PROJECT_DIR, "forge_presentation_neural.py")

# ─────────────────────────────────────────────
# 🧠 Utility Routines
# ─────────────────────────────────────────────
def run_command(cmd, output_widget):
    """Execute system command and stream output to the UI."""
    process = subprocess.Popen(
        ["python", cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    for line in process.stdout:
        output_widget.insert(tk.END, line)
        output_widget.see(tk.END)
    process.wait()

def threaded_run(cmd, output_widget):
    t = threading.Thread(target=run_command, args=(cmd, output_widget), daemon=True)
    t.start()

# ─────────────────────────────────────────────
# 🪄 UI Setup
# ─────────────────────────────────────────────
def launch_ui():
    root = tk.Tk()
    root.title("💎 Realms to Riches | Agentic Master Forge UI")
    root.geometry("900x600")
    root.configure(bg="#111111")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Consolas", 11, "bold"), padding=8)

    # Title
    title = tk.Label(
        root,
        text="💎 REALMS TO RICHES | AGENTIC MASTER FORGE",
        font=("Consolas", 14, "bold"),
        bg="#111111",
        fg="#00FFFF",
    )
    title.pack(pady=10)

    # Button frame
    btn_frame = tk.Frame(root, bg="#111111")
    btn_frame.pack(pady=10)

    ttk.Button(
        btn_frame, text="🚀 Launch Forge System",
        command=lambda: threaded_run(FORGE_LAUNCH, output_box)
    ).grid(row=0, column=0, padx=5)

    ttk.Button(
        btn_frame, text="🎬 Launch Forge Cinematic",
        command=lambda: threaded_run(CINEMATIC, output_box)
    ).grid(row=0, column=1, padx=5)

    ttk.Button(
        btn_frame, text="🧩 Exit",
        command=root.destroy
    ).grid(row=0, column=2, padx=5)

    # Output box
    output_box = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, width=110, height=25, bg="#000000", fg="#00FFAA",
        insertbackground="white", font=("Consolas", 10)
    )
    output_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    launch_ui()