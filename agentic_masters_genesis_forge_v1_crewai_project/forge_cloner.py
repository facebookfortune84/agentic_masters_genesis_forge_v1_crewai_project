import os, shutil

def clone_forge_template(timestamp):
    src_root = os.getcwd()
    dst_root = os.path.join("deliverables", f"run_{timestamp}")
    os.makedirs(dst_root, exist_ok=True)

    include = [
        "config", "tools", "knowledge", "crew.py", "main.py",
        ".env.template", "pyproject.toml", "README.md", "ui"
    ]

    for item in include:
        src_path = os.path.join(src_root, item)
        dst_path = os.path.join(dst_root, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        elif os.path.isfile(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)