import os, yaml

def inject(timestamp, agents, tasks):
    config_path = os.path.join("deliverables", f"run_{timestamp}", "config")
    os.makedirs(config_path, exist_ok=True)

    with open(os.path.join(config_path, "agents.yaml"), "w", encoding="utf-8") as f:
        yaml.dump({"agents": agents}, f, sort_keys=False)

    with open(os.path.join(config_path, "tasks.yaml"), "w", encoding="utf-8") as f:
        yaml.dump({"tasks": tasks}, f, sort_keys=False)