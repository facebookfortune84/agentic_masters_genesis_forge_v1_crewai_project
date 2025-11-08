#!/usr/bin/env python3
"""
Builds a detailed tasks.yaml linking each agent to one or more tasks.
Each task has longform guidance and output validation notes.
"""

import yaml, os

tasks = {"tasks": []}

def task(agent_name, title, description, output_file):
    return {
        "agent": agent_name,
        "title": title,
        "instructions": description,
        "output": {
            "file": f"deliverables/{output_file}",
            "format": "markdown",
            "validation": [
                "Syntax linting",
                "Unit test execution",
                "Integration verification",
                "Peer review by adjacent team"
            ]
        }
    }

# Core forge construction sequence
phases = [
    ("Architect", "Forge Core Blueprint", 
     "Design the neural forge core architecture, including data pipelines, "
     "execution environment, and memory management subsystems."),
    ("Compiler", "Language Genesis",
     "Draft the syntax, semantics, and grammar of the new Forge programming language."),
    ("System Analyst", "Diagnostics Engine",
     "Develop real-time system diagnostics and fault-detection modules."),
    ("Data Engineer", "Knowledge Pipeline",
     "Create ingestion and preprocessing pipelines for internal and external data."),
    ("Language Designer", "Language Specification",
     "Formalize tokenization, parsing, and AST handling."),
    ("Security Auditor", "Security Framework",
     "Implement multi-layer validation, sandboxing, and key management."),
    ("AI Trainer", "Agent Training Suite",
     "Develop prompt libraries, validation datasets, and fine-tuning workflow."),
    ("Testing Engineer", "Testing Framework",
     "Build pytest/unittest-based frameworks and CI/CD hooks."),
    ("Integration Specialist", "System Integration",
     "Integrate all forge components, verify dependencies, and deploy simulation."),
    ("Neural Broadcaster", "Presentation Layer",
     "Create narrative presentation and voice integration scripts.")
]

for team in range(1, 21):
    for role, title, desc in phases:
        agent_name = f"{role} {team}-{phases.index((role,title,desc))+1}"
        tasks["tasks"].append(
            task(agent_name, title, f"[Team {team}] {desc}", f"{title.replace(' ', '_').lower()}_team{team}.md")
        )

os.makedirs("src/agentic_masters_genesis_forge/config", exist_ok=True)
out = "src/agentic_masters_genesis_forge/config/tasks.yaml"
with open(out, "w", encoding="utf-8") as f:
    yaml.dump(tasks, f, sort_keys=False)
print(f"✅ Generated {len(tasks['tasks'])} tasks into {out}")