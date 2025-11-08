#!/usr/bin/env python3
"""
Generates a fully expanded agents.yaml for the Realms to Riches Forge.
Creates 20 teams of 10 agents each with structured roles.
"""

import yaml, os, random

ROLES = [
    "Architect", "Compiler", "System Analyst", "Data Engineer",
    "Language Designer", "Security Auditor", "AI Trainer",
    "Testing Engineer", "Integration Specialist", "Neural Broadcaster"
]

agents = {"agents": []}
for team in range(1, 21):
    for i, role in enumerate(ROLES, start=1):
        agent = {
            "id": f"T{team:02d}_A{i:02d}",
            "name": f"{role} {team}-{i}",
            "team": f"Team {team}",
            "role": role,
            "description": f"{role} responsible for the {role.lower()} phase of Forge development.",
            "capabilities": [
                "Autonomous reasoning", "Tool execution", "Report generation",
                "Source-code synthesis", "Self-validation"
            ],
            "tools": [
                "custom_tool.py",
                "forge_project/performance_overdrive.py",
                "forge_project/forge_master_runner.py"
            ],
            "memory_file": "memory/crew_memory.json",
            "output_dir": f"deliverables/team_{team}",
        }
        agents["agents"].append(agent)

os.makedirs("src/agentic_masters_genesis_forge/config", exist_ok=True)
out = "src/agentic_masters_genesis_forge/config/agents.yaml"
with open(out, "w", encoding="utf-8") as f:
    yaml.dump(agents, f, sort_keys=False)
print(f"✅ Generated {len(agents['agents'])} agents into {out}")