import yaml, os

def validate_yaml(path, expected_key):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if isinstance(data, dict) and expected_key in data:
        items = data[expected_key]
    else:
        items = data

    if not isinstance(items, (list, dict)):
        print(f"❌ {expected_key}.yaml is not a list or dict.")
        return []

    if isinstance(items, dict):
        return [{"id": k, **v} for k, v in items.items() if isinstance(v, dict)]
    return items

def list_items(items, label):
    print(f"\n🧠 Listing {len(items)} {label}:\n")
    for item in items:
        print(f"- {item.get('id', 'unknown')}")

def main():
    agents_path = os.path.join("config", "agents.yaml")
    tasks_path = os.path.join("config", "tasks.yaml")

    agents = validate_yaml(agents_path, "agents")
    tasks = validate_yaml(tasks_path, "tasks")

    list_items(agents, "agents")
    list_items(tasks, "tasks")

if __name__ == "__main__":
    main()