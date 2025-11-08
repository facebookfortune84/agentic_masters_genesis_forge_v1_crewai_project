#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ Crew Manager
Manages all 200 agents across 20 teams, loads configuration, assigns tasks, and autoheals errors.
"""

import os, yaml, json, random, time, traceback
from colorama import Fore, Style

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
MEMORY_PATH = os.path.join(BASE_DIR, "memory", "crew_memory.json")

class ForgeAgent:
    def __init__(self, data):
        self.id = data.get("id")
        self.name = data.get("name")
        self.role = data.get("role")
        self.voice = data.get("voice", "Adam")
        self.deliverable_focus = data.get("deliverable_focus")
        self.dossier = data.get("dossier", {})
        self.performance = {"tasks_completed": 0, "errors": 0}

    def perform_task(self, task):
        try:
            task_name = task.get("name") or task.get("title") or "Unnamed Task"
            print(Fore.CYAN + f"🧠 {self.name} executing: {task_name}")
            time.sleep(0.2)
            if random.random() < 0.95:
                self.performance["tasks_completed"] += 1
                return {
                    "agent_id": self.id,
                    "task_id": task.get("id", "unknown"),
                    "status": "completed",
                    "timestamp": time.time()
                }
            else:
                raise RuntimeError("Simulated execution error")
        except Exception as e:
            self.performance["errors"] += 1
            return {
                "agent_id": self.id,
                "task_id": task.get("id", "unknown"),
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": time.time()
            }

class CrewManager:
    def __init__(self):
        self.agents = []
        self.tasks = []
        self.memory = {}
        self.load_configs()
        self.load_memory()

    def load_configs(self):
        with open(os.path.join(CONFIG_DIR, "agents.yaml"), encoding="utf-8") as f:
            agents_data = yaml.safe_load(f)
            self.agents = agents_data["agents"] if isinstance(agents_data, dict) and "agents" in agents_data else agents_data

        with open(os.path.join(CONFIG_DIR, "tasks.yaml"), encoding="utf-8") as f:
            tasks_data = yaml.safe_load(f)
            raw_tasks = tasks_data["tasks"] if isinstance(tasks_data, dict) and "tasks" in tasks_data else tasks_data

            if isinstance(raw_tasks, dict):
                self.tasks = [
                    {"id": task_id, **task_info}
                    for task_id, task_info in raw_tasks.items()
                    if isinstance(task_info, dict)
                ]
            elif isinstance(raw_tasks, list):
                self.tasks = [
                    task if "id" in task else {**task, "id": f"task_{i+1}"}
                    for i, task in enumerate(raw_tasks)
                    if isinstance(task, dict)
                ]
            else:
                raise ValueError("Invalid tasks.yaml format: must be list or dict")

        print(Fore.GREEN + f"✅ Loaded {len(self.agents)} agents and {len(self.tasks)} tasks.")

    def load_memory(self):
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = {"runs": []}

    def assign_and_execute(self):
        print(Fore.MAGENTA + "\n🚀 Assigning tasks to teams...\n")
        results = []
        for agent_data in self.agents:
            agent = ForgeAgent(agent_data)
            assigned_tasks = random.sample(self.tasks, min(3, len(self.tasks)))
            for task in assigned_tasks:
                result = agent.perform_task(task)
                results.append(result)
                if result["status"] == "error":
                    self.delegate_repair(agent, task, result)
        self.memory["runs"].append({
            "timestamp": time.time(),
            "results": results,
            "agents": [a["id"] for a in self.agents],
            "tasks": [t["id"] for t in self.tasks]
        })
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)
        print(Fore.YELLOW + f"\n📊 {len(results)} task instances executed.\n")

    def delegate_repair(self, failed_agent, failed_task, error_result):
        fallback_data = random.choice(self.agents)
        fallback_agent = ForgeAgent(fallback_data)
        task_name = failed_task.get("name") or failed_task.get("title") or "Unnamed Task"
        print(Fore.RED + f"⚠️ {failed_agent.name} failed task '{task_name}'. Delegating to {fallback_agent.name}...")
        instructions = f"Fix error: {error_result['error']}\nTraceback:\n{error_result['traceback']}"
        time.sleep(0.2)
        print(Fore.BLUE + f"🛠️ {fallback_agent.name} received instructions:\n{instructions}")
        retry_result = fallback_agent.perform_task(failed_task)

    # Ensure memory["runs"] exists
        if "runs" not in self.memory or not self.memory["runs"]:
            self.memory["runs"] = [{"timestamp": time.time(), "results": []}]

        self.memory["runs"][-1]["results"].append(retry_result)



