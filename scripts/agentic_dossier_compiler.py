import yaml, random, os
from collections import defaultdict

# === PATHS ===
PREFILL_PATH = "ui/prefill_mappings.yaml"
BACKUP_PATH = "ui/backup/prefill_mappings_backup.yaml"
TEAMS_PATH = "ui/teams.yaml"
MASTER_FORGE_PATH = "ui/master_forge.yaml"

# === CONFIG ===
ROLE_TO_TEAM = {
    "Audit": "Governance", "Memory": "Memory & Context", "Dispatch": "Dispatch & Routing",
    "Tone": "UX & Tone", "Credential": "Credential Hygiene", "Packaging": "Packaging & CI/CD",
    "Onboarding": "Onboarding & Persona", "Feedback": "Feedback & Optimization",
    "Privacy": "Legal & Privacy", "Retention": "Memory & Context", "Variant": "UX & Tone",
    "Transparency": "Governance", "Engagement": "Feedback & Optimization", "Bias": "Governance",
    "Governance": "Governance", "Redaction": "Credential Hygiene", "Token": "Credential Hygiene",
    "Consent": "Legal & Privacy", "FOIA": "Legal & Privacy", "eDiscovery": "Legal & Privacy"
}

TOOLS_BY_EXTENSION = {
    "py": ["Python", "Debugger", "Validator"], "json": ["JSON", "Registry", "Tracker"],
    "yaml": ["YAML", "Pipeline", "Protocol"], "md": ["Markdown", "Documentation"],
    "txt": ["Text Parser", "Prompt Designer"], "csv": ["CSV", "Log Exporter"],
    "html": ["HTML", "Web Renderer"], "js": ["JavaScript", "Frontend"], "zip": ["Bundler", "Packager"]
}

PHYSICAL_FORMS = ["Hologram", "Avatar", "Drone", "Console", "Terminal", "Floating HUD", "AR Panel"]

# === UTILS ===
def generate_name():
    first = random.choice(["Nova", "Echo", "Zara", "Axel", "Kai", "Luna", "Orion", "Juno", "Rex", "Vega"])
    last = random.choice(["Prime", "Core", "Flux", "Drift", "Pulse", "Forge", "Trace", "Spark", "Byte", "Node"])
    return f"{first} {last}"

def infer_team(role):
    for keyword, team in ROLE_TO_TEAM.items():
        if keyword.lower() in role.lower():
            return team
    return "General Ops"

def infer_tools(tasks):
    tools = set()
    for task in tasks:
        ext = task.get("file_type", "")
        tools.update(TOOLS_BY_EXTENSION.get(ext, []))
    return sorted(tools)

def infer_persona(role):
    if "Audit" in role or "Governance" in role:
        return "Strict compliance enforcer with zero tolerance for ambiguity"
    if "Memory" in role:
        return "Long-context strategist with deep recall and semantic threading"
    if "Dispatch" in role:
        return "Fast-routing tactician with fallback logic and verification rituals"
    if "Tone" in role or "UX" in role:
        return "Empathic communicator tuned for multilingual emotional resonance"
    return "Modular agent with adaptive orchestration capabilities"

def infer_rate(tools):
    base = 35
    return base + len(tools) * 5

# === MAIN ===
def compile_dossier():
    # Ensure backup folder exists
    os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)

    # Backup original
    if os.path.exists(PREFILL_PATH):
        with open(PREFILL_PATH, "r") as f:
            original = f.read()
        with open(BACKUP_PATH, "w") as f:
            f.write(original)
        print("📦 Backup saved to ui/backup/prefill_mappings_backup.yaml")

    # Load agents
    with open(PREFILL_PATH, "r") as f:
        agents = yaml.safe_load(f)

    if not isinstance(agents, list):
        print("❌ ERROR: prefill_mappings.yaml must be a top-level list of agent dictionaries.")
        return

    enriched_agents = []
    teams = defaultdict(list)

    for i, agent in enumerate(agents, start=1):
        if not isinstance(agent, dict):
            print(f"⚠️ Skipping non-dict entry at index {i}: {type(agent)}")
            continue
        if "role" not in agent or "tasks" not in agent:
            print(f"⚠️ Skipping incomplete agent at index {i}: missing 'role' or 'tasks'")
            continue

        agent["employee_id"] = f"AGENT-{i:04d}"
        agent["name"] = generate_name()
        agent["team"] = infer_team(agent["role"])
        agent["persona"] = infer_persona(agent["role"])
        agent["tools_assigned"] = infer_tools(agent["tasks"])
        agent["hourly_rate"] = infer_rate(agent["tools_assigned"])
        agent["physical_form"] = random.choice(PHYSICAL_FORMS)

        enriched_agents.append(agent)
        teams[agent["team"]].append(agent["role"])

        print(f"✅ Enriched agent {agent['employee_id']}: {agent['role']} → Team: {agent['team']}")

    # Write enriched mappings
    with open(PREFILL_PATH, "w") as f:
        yaml.dump(enriched_agents, f, sort_keys=False)
    with open(TEAMS_PATH, "w") as f:
        yaml.dump(dict(teams), f, sort_keys=False)
    with open(MASTER_FORGE_PATH, "w") as f:
        yaml.dump(enriched_agents, f, sort_keys=False)

    print("\n🎯 Dossier compilation complete:")
    print(f"→ Enriched agents written to: {PREFILL_PATH}")
    print(f"→ Teams written to: {TEAMS_PATH}")
    print(f"→ Master Forge written to: {MASTER_FORGE_PATH}")

if __name__ == "__main__":
    compile_dossier()