#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Forge YAML Rebuilder — Synchronizes agent/task configurations
────────────────────────────────────────────────────────────
"""

import os, yaml

AGENTS = [
    {"name": "Adam Orchestrator", "role": "Command Overseer", "voice": "Adam"},
    {"name": "Charlotte", "role": "Narrative Architect"},
    {"name": "Roger", "role": "Systems Analyst"},
    {"name": "Elli", "role": "Deliverables Manager"},
]

TASKS = [
    {"name": "Launch Forge", "description": "Initiate system launch", "agent": "Adam Orchestrator"},
    {"name": "Validate Deliverables", "description": "Run full validation check", "agent": "Elli"},
    {"name": "Rebuild Environment", "description": "Reset and relaunch environment", "agent": "Roger"},
    {"name": "Narrate Presentation", "description": "Deliver neural presentation", "agent": "Charlotte"},
]

def rebuild_yaml():
    root = os.path.dirname(os.path.abspath(__file__))
    agents_path = os.path.join(root, "agents.yaml")
    tasks_path = os.path.join(root, "tasks.yaml")
    with open(agents_path, "w", encoding="utf-8") as f:
        yaml.dump(AGENTS, f)
    with open(tasks_path, "w", encoding="utf-8") as f:
        yaml.dump(TASKS, f)
    print(f"✅ YAML files rebuilt:\n - {agents_path}\n - {tasks_path}")

if __name__ == "__main__":
    rebuild_yaml()