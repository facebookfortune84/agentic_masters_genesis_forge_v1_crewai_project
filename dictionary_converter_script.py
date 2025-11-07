def wrap_yaml(file_path, wrapper_key):
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()
    indented = ["  " + line if line.strip() else line for line in lines]
    wrapped = [f"{wrapper_key}:\n"] + indented
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(wrapped)

wrap_yaml("config/agents.yaml", "agents")
wrap_yaml("config/tasks.yaml", "tasks")