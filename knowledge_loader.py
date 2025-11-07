import os, json, random
from colorama import Fore

def load_knowledge():
    print(Fore.CYAN + "📚 Loading Forge Knowledge Base...")
    knowledge_dir = os.path.join("src","agentic_masters_genesis_forge","knowledge")
    os.makedirs(knowledge_dir, exist_ok=True)
    core_knowledge = ["compiler design","neural architecture","autonomous agents","python metaprogramming"]
    with open(os.path.join(knowledge_dir, "core_knowledge.json"), "w") as f:
        json.dump(core_knowledge, f)
    print(Fore.GREEN + "✅ Knowledge base loaded.")