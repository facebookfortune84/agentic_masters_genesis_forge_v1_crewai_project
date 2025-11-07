# -*- coding: utf-8 -*-
"""
🩺 Diagnostics Forger — reads logs & diagnoses Forge malfunctions
"""
import os, datetime, io, sys
from colorama import Fore, Style, init
init(autoreset=True)

# Fix Unicode printing on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

def scan_log(log_dir="deliverables"):
    log_file = os.path.join(log_dir, "orchestrator_log.txt")
    print(Fore.CYAN + f"🩺 Scanning log file: {log_file}")
    if not os.path.exists(log_file):
        print(Fore.YELLOW + "⚠️ No orchestrator_log.txt found.")
        return {"status": "missing"}

    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[-30:]

    print(Fore.MAGENTA + "\n─ Recent Log Excerpt ─")
    for line in lines:
        print(Fore.WHITE + line.strip())
    print(Fore.MAGENTA + "─ End of Log ─\n")

    crash_lines = [l for l in lines if "Traceback" in l or "Error" in l or "Exception" in l]
    if crash_lines:
        print(Fore.RED + f"💥 {len(crash_lines)} error events detected.")
        return {"status": "errors", "errors": crash_lines}
    print(Fore.GREEN + "✅ No fatal errors detected.")
    return {"status": "clean"}