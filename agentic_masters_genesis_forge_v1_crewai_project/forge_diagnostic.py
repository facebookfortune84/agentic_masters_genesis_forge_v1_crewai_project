#!/usr/bin/env python3
"""
Realms to Riches | Forge Diagnostic Probe
──────────────────────────────────────────
Scans the entire Forge workspace to verify that:
 - Agent tasks executed (non-empty stdout)
 - Deliverables folder paths are valid
 - Output files actually created and timestamped
 - Latest run produced new content
"""
import os, json, time, re, glob, datetime
from colorama import Fore, Style, init
init(autoreset=True)

DELIVERABLES = "deliverables"
LOGS = glob.glob("**/*.log", recursive=True)

def recent_files(base=DELIVERABLES, minutes=30):
    now = time.time()
    files = []
    for p in glob.glob(os.path.join(base, "*.md")):
        if os.path.getmtime(p) > now - minutes*60:
            files.append(p)
    return files

def analyze_last_run():
    print(Fore.CYAN + "\n🔍 Checking recent deliverables…")
    recents = recent_files()
    if not recents:
        print(Fore.RED + "❌ No new deliverables in last 30 min.")
    else:
        for f in recents:
            size = os.path.getsize(f)
            print(Fore.GREEN + f"✅ {f} — {size} bytes")

    print(Fore.CYAN + "\n🧩 Scanning logs for agent activity…")
    hits = 0
    for log in LOGS:
        txt = open(log, errors="ignore").read()
        if "Final Answer" in txt or "Task Completed" in txt:
            hits += 1
    print(Fore.GREEN + f"Agent output signatures: {hits}")

    if hits == 0:
        print(Fore.YELLOW + "⚠️ Agents may not be running or writing output.")
    print(Fore.WHITE + "\nDiagnostic complete.\n")

if __name__ == "__main__":
    analyze_last_run()