import os, json
from colorama import Fore

def initialize_teams():
    print(Fore.CYAN + "🧠 Initializing 20 Forge Teams...")
    structure = {f"Team_{i}": {"agents": [f"Agent_{i}_{j}" for j in range(1,11)]} for i in range(1,21)}
    os.makedirs("memory", exist_ok=True)
    with open("memory/team_structure.json","w") as f:
        json.dump(structure, f, indent=2)
    print(Fore.GREEN + "✅ All teams initialized successfully.")