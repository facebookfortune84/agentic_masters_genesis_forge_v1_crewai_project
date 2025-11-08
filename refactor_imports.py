import os
import re

# Define your package root
PACKAGE_NAME = "agentic_masters_genesis_forge_v1_crewai_project"

# Map old module names to new ones
IMPORT_MAP = {
    "crew": f"{PACKAGE_NAME}.crew",
    "main": f"{PACKAGE_NAME}.main",
    "forge_cloner": f"{PACKAGE_NAME}.forge_cloner",
    "forge_diagnostic": f"{PACKAGE_NAME}.forge_diagnostic",
    "inject_config": f"{PACKAGE_NAME}.inject_config",
    "inject_env_and_pyproject": f"{PACKAGE_NAME}.inject_env_and_pyproject",
    "validate_forge": f"{PACKAGE_NAME}.validate_forge",
    "validate_yaml": f"{PACKAGE_NAME}.validate_yaml",
    "multi_team_initializer": f"{PACKAGE_NAME}.multi_team_initializer"
}

# Regex to match import statements
IMPORT_REGEX = re.compile(r"from\s+(\w+)\s+import\s+(.*)")

def refactor_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    changed = False

    for line in lines:
        match = IMPORT_REGEX.match(line.strip())
        if match:
            old_module, symbols = match.groups()
            if old_module in IMPORT_MAP:
                new_module = IMPORT_MAP[old_module]
                new_line = f"from {new_module} import {symbols}\n"
                updated_lines.append(new_line)
                changed = True
                print(f"🔁 Replaced in {path}: {line.strip()} → {new_line.strip()}")
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

def scan_repo(root="."):
    for dirpath, _, filenames in os.walk(root):
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                refactor_file(full_path)

if __name__ == "__main__":
    print("🔍 Scanning repo for outdated imports...")
    scan_repo()
    print("✅ Import refactor complete.")