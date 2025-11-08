import os, re, json
from glob import glob

DELIVERABLES = "deliverables"
parsed = []

for path in glob(f"{DELIVERABLES}/*.md"):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Basic classification
    project_code = re.findall(r'```(.*?)```', text, re.DOTALL)
    dossier_title = re.findall(r'# (.*?)\n', text)
    parsed.append({
        "file": os.path.basename(path),
        "title": dossier_title[0] if dossier_title else "",
        "code_blocks": project_code,
        "summary": text[:600] + "..." if len(text) > 600 else text
    })

with open("forge_index.json", "w", encoding="utf-8") as out:
    json.dump(parsed, out, indent=2)

print(f"✅ Parsed {len(parsed)} deliverables -> forge_index.json")