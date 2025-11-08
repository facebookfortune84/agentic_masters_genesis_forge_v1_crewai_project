import yaml, os

TASKS_PATH = os.path.join("config", "tasks.yaml")

def load_tasks():
    with open(TASKS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Handle double-wrapped structure: tasks: tasks: [...]
    if isinstance(data, dict) and "tasks" in data:
        inner = data["tasks"]
        if isinstance(inner, dict) and "tasks" in inner:
            tasks = inner["tasks"]
        else:
            tasks = inner
    else:
        tasks = data

    # Normalize to list
    if isinstance(tasks, dict):
        tasks = [{"id": k, **v} for k, v in tasks.items() if isinstance(v, dict)]
    elif isinstance(tasks, list):
        tasks = [
            task if "id" in task else {**task, "id": f"task_{i+1}"}
            for i, task in enumerate(tasks)
            if isinstance(task, dict)
        ]
    else:
        raise ValueError("Invalid tasks.yaml format")

    return tasks

def save_tasks(tasks):
    with open(TASKS_PATH, "w", encoding="utf-8") as f:
        yaml.dump({"tasks": tasks}, f, sort_keys=False, allow_unicode=True)

def list_tasks(tasks):
    print(f"\n🧠 Listing {len(tasks)} tasks:\n")
    for task in tasks:
        print(f"- {task['id']}")

def main():
    tasks = load_tasks()
    save_tasks(tasks)
    list_tasks(tasks)

if __name__ == "__main__":
    main()