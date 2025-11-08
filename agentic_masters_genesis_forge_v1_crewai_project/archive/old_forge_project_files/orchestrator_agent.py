#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🧠 Realms to Riches | Orchestrator Agent V2
──────────────────────────────────────────────
Executive command interface for the Agentic Master Forge system.

Roles:
- CEO Command Interpreter
- Subsystem Orchestrator
- Agent Liaison (Messenger)
- Validator & Diagnostics Officer
──────────────────────────────────────────────
"""

import os, sys, json, re, time, subprocess, datetime, threading, queue
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────
# 📁 Path Setup
# ─────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
for p in (ROOT, PARENT):
    if p not in sys.path:
        sys.path.insert(0, p)

# ─────────────────────────────────────────────
# 🔧 Safe Imports (Diagnostics + Validator)
# ─────────────────────────────────────────────
try:
    from diagnostics_forger import scan_log
except ImportError:
    def scan_log():
        return {"status": "missing", "message": "diagnostics_forger not available"}

try:
    from forge_validator import validate_forge_output
except ImportError:
    def validate_forge_output(path):
        return {"status": "skipped", "message": "forge_validator not found"}

# ─────────────────────────────────────────────
# 🧠 Orchestrator Core Class
# ─────────────────────────────────────────────
class OrchestratorAgent:
    def __init__(self, root="."):
        self.root = os.path.abspath(root)
        self.deliverables = os.path.join(self.root, "deliverables")
        os.makedirs(self.deliverables, exist_ok=True)
        self.log_path = os.path.join(self.deliverables, "orchestrator_v2_log.txt")
        self.message_queue = queue.Queue()
        self.state = {"last_action": None, "deliverables": 0, "status": "idle"}

        self.log("🧠 Orchestrator online — awaiting command input...", Fore.CYAN)

    # ─────────────────────────────
    def log(self, msg, color=Fore.CYAN):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(color + line + Style.RESET_ALL)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # ─────────────────────────────
    def execute(self, cmd):
        """Executes a shell command safely with logging."""
        self.log(f"⚙️ Executing: {cmd}", Fore.YELLOW)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.stdout:
                self.log(result.stdout.strip(), Fore.GREEN)
            if result.stderr:
                self.log(result.stderr.strip(), Fore.RED)
            return result.returncode == 0
        except Exception as e:
            self.log(f"💥 Execution failed: {e}", Fore.RED)
            return False

    # ─────────────────────────────
    # 🎯 Command Dispatcher
    # ─────────────────────────────
    def handle_command(self, text):
        """Natural-language command interpreter."""
        text = text.lower().strip()
        if not text:
            return

        # CEO-style speech patterns → actions
        if re.search(r"\bdiagnos(e|tics)?\b", text):
            self.diagnose()
        elif re.search(r"\bvalidate|check\b", text):
            self.validate()
        elif re.search(r"\brebuild|reset|reinit\b", text):
            self.rebuild()
        elif re.search(r"\blaunch|start|ignite|run\b", text):
            self.launch_forge()
        elif re.search(r"\bmessage|tell|inform|update\b", text):
            self.relay_message(text)
        elif re.search(r"\blog|report|status|summary\b", text):
            self.show_status()
        elif re.search(r"\bhelp|commands\b", text):
            self.help()
        else:
            self.log("🤔 Command not recognized. Type 'help' for available actions.", Fore.YELLOW)

    # ─────────────────────────────
    # 🧩 Core Actions
    # ─────────────────────────────
    def diagnose(self):
        self.log("🔍 Running Forge diagnostics...")
        result = scan_log()
        self.log(json.dumps(result, indent=2), Fore.CYAN)
        self.state["last_action"] = "diagnose"

    def validate(self):
        self.log("🧪 Validating Forge deliverables...")
        result = validate_forge_output(self.deliverables)
        self.log(json.dumps(result, indent=2), Fore.CYAN)
        self.state["last_action"] = "validate"

    def rebuild(self):
        self.log("🧰 Rebuilding Forge system launch environment...")
        self.execute("python forge_project/forge_system_launch.py")
        self.state["last_action"] = "rebuild"

    def launch_forge(self):
        self.log("🚀 Launching Realms to Riches Forge pipeline...")
        self.execute("python forge_project/forge_system_launch.py")
        self.state["last_action"] = "launch"

    # ─────────────────────────────
    # 🗣️ Internal Messaging System
    # ─────────────────────────────
    def relay_message(self, text):
        """Simulates sending an instruction to an agent."""
        agent_match = re.search(r"to ([a-z0-9_]+)", text)
        msg_match = re.search(r"say|tell|to [^ ]+ (.+)", text)
        agent = agent_match.group(1) if agent_match else "forge_team"
        message = msg_match.group(1) if msg_match else text

        entry = {"agent": agent, "message": message, "time": datetime.datetime.now().isoformat()}
        self.message_queue.put(entry)
        self.log(f"📨 Message queued for {agent}: {message}", Fore.MAGENTA)

    # ─────────────────────────────
    # 📊 Status + Help
    # ─────────────────────────────
    def show_status(self):
        self.log("📋 Forge Orchestrator Status Report", Fore.CYAN)
        for k, v in self.state.items():
            self.log(f"{k}: {v}", Fore.WHITE)
        self.log(f"Pending Messages: {self.message_queue.qsize()}", Fore.CYAN)

    def help(self):
        self.log("""
🧭 Available Commands:
───────────────────────────────
launch forge        → Run full neural system launch
diagnose forge      → Run diagnostics_forger
validate outputs    → Validate deliverables
rebuild forge       → Clean + rebuild system
message [agent] ... → Send instruction to an agent
status / report     → Show orchestrator state
help / commands     → Show this help menu
───────────────────────────────
Example:
> tell charlotte to rebuild presentation visuals
> launch forge and validate results
> show status
""", Fore.CYAN)

# ─────────────────────────────
# 🧩 CLI Entry
# ─────────────────────────────
if __name__ == "__main__":
    orch = OrchestratorAgent(".")
    orch.help()

    while True:
        try:
            cmd = input(Fore.YELLOW + "\n🧠 CEO> " + Style.RESET_ALL)
            if cmd.lower().strip() in ("exit", "quit"):
                orch.log("🧩 Session terminated. Goodbye Commander.", Fore.CYAN)
                break
            orch.handle_command(cmd)
        except KeyboardInterrupt:
            orch.log("\n🧩 Orchestrator session interrupted.", Fore.RED)
            break