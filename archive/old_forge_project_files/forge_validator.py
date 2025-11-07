# -*- coding: utf-8 -*-
"""
🔍 Forge Validator — validates deliverable structure & integrity
"""
import os, json, datetime
from colorama import Fore, Style

def validate_forge_output(deliverables_path="deliverables"):
    print(Fore.CYAN + f"🔎 Validating deliverables in: {deliverables_path}")
    if not os.path.exists(deliverables_path):
        print(Fore.RED + "❌ Deliverables folder missing.")
        return {"status": "failed"}

    files = [f for f in os.listdir(deliverables_path)
             if f.endswith((".md", ".json", ".txt"))]
    if not files:
        print(Fore.YELLOW + "⚠️ No deliverables detected.")
        return {"status": "empty"}

    report = []
    for f in files:
        path = os.path.join(deliverables_path, f)
        size = os.path.getsize(path)
        if size == 0:
            print(Fore.YELLOW + f"⚠️ Empty file: {f}")
        else:
            print(Fore.GREEN + f"✅ {f} — {size} bytes")
        report.append({"file": f, "size": size})

    manifest = os.path.join(deliverables_path, "validation_manifest.json")
    json.dump(report, open(manifest, "w", encoding="utf-8"), indent=2)
    print(Fore.CYAN + Style.BRIGHT + "📜 Validation complete.")
    return {"status": "complete", "files": len(report)}