import os, yaml

REQUIRED_FOLDERS = ["config", "tools", "knowledge", "ui"]
REQUIRED_FILES = [
    "config/agents.yaml",
    "config/tasks.yaml",
    "crew.py",
    "main.py",
    ".env.template",
    "pyproject.toml"
]

def validate_yaml(path, key):
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and key in data:
            return True
        return False
    except Exception:
        return False

def validate_forge(path):
    print(f"\n🔍 Validating Forge at: {path}\n")

    # Check folders
    for folder in REQUIRED_FOLDERS:
        if not os.path.isdir(os.path.join(path, folder)):
            print(f"❌ Missing folder: {folder}")
        else:
            print(f"✅ Found folder: {folder}")

    # Check files
    for file in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(path, file)):
            print(f"❌ Missing file: {file}")
        else:
            print(f"✅ Found file: {file}")

    # Validate YAML
    agents_ok = validate_yaml(os.path.join(path, "config", "agents.yaml"), "agents")
    tasks_ok = validate_yaml(os.path.join(path, "config", "tasks.yaml"), "tasks")

    print(f"🧠 Agents.yaml valid: {'✅' if agents_ok else '❌'}")
    print(f"📋 Tasks.yaml valid: {'✅' if tasks_ok else '❌'}")

    # Validate pyproject.toml
    try:
        with open(os.path.join(path, "pyproject.toml"), encoding="utf-8") as f:
            content = f.read()
        if "[project]" in content and "name =" in content:
            print("📦 pyproject.toml format: ✅")
        else:
            print("📦 pyproject.toml format: ❌")
    except Exception:
        print("📦 pyproject.toml format: ❌")

    print("\n✅ Validation complete.\n")

if __name__ == "__main__":
    target = input("Enter path to Forge (e.g., deliverables/run_20251106_1500): ")
    validate_forge(target)