#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 REALMS TO RICHES | ADAM v5 DEPLOYER — FAILSAFE MODE
───────────────────────────────────────────────────────
Automatically:
✅ Repairs blueprint BOM or missing file
✅ Rebuilds orchestrator_conscious_v5.py
✅ Validates environment and deploys Adam
───────────────────────────────────────────────────────
"""

import os, json, sys, datetime, subprocess,
from colorama import Fore, Style, init
init(autoreset=True)

# UTF-8 fix for Windows consoles
if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

from forge_validator import validate_forge_output
from diagnostics_forger import scan_log

ROOT = os.getcwd()
FORGE_DIR = os.path.join(ROOT, "forge_project")
BLUEPRINT = os.path.join(FORGE_DIR, "orchestrator_conscious_v5_blueprint.json")
TARGET = os.path.join(FORGE_DIR, "orchestrator_conscious_v5.py")

# ───────────────────────────────────────────────
# 💾 Utility Functions
# ───────────────────────────────────────────────
def log(msg, color=Fore.CYAN):
    print(color + msg + Style.RESET_ALL)
    sys.stdout.flush()

def safe_load_json(path):
    """Load a JSON file safely, stripping BOM if needed."""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        log(f"⚠️  Failed to load {os.path.basename(path)}: {e}", Fore.YELLOW)
        return None

def write_blueprint():
    """Rebuild Adam v5 blueprint."""
    os.makedirs(FORGE_DIR, exist_ok=True)
    log("🧠 Rebuilding Adam v5 blueprint...", Fore.YELLOW)
    blueprint = {
        "name": "Adam v5",
        "description": "Autonomous Orchestrator with healing, RAG, and self-diagnostics",
        "modes": ["diagnostic", "forge_healing", "conversation", "training"],
        "speech": {"primary": "elevenlabs", "fallback": "pyttsx3"},
        "memory": {"enabled": True, "path": "memory/adam_v5_memory.json"},
        "rag": {"enabled": True, "sources": ["agents.yaml", "tasks.yaml", "deliverables/"]},
        "objectives": [
            "Diagnose missing deliverables",
            "Heal Forge process",
            "Coordinate with reactive agents",
            "Maintain voice conversation with Commander"
        ]
    }
    with open(BLUEPRINT, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, indent=2)
    log(f"✅ Blueprint rebuilt → {BLUEPRINT}", Fore.GREEN)
    return blueprint

# ───────────────────────────────────────────────
# 🧠 Build the Orchestrator File
# ───────────────────────────────────────────────
def generate_orchestrator(blueprint):
    """Write orchestrator_conscious_v5.py"""
    log("🧩 Generating orchestrator_conscious_v5.py...", Fore.CYAN)
    script = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💠 Adam v5 — Conscious Orchestrator
────────────────────────────────────────────
Role: Autonomous Forge Coordinator
Modes: {", ".join(blueprint["modes"])}
────────────────────────────────────────────
"""

import os, json, sys, time, threading, requests, subprocess
from colorama import Fore, Style, init
init(autoreset=True)

from forge_validator import validate_forge_output
from forge_presentation_neural import analyze_deliverables
from diagnostics_forger import scan_log

try:
    import pyttsx3
    import speech_recognition as sr
except ImportError:
    print(Fore.RED + "⚠️ Required speech packages missing. Run: pip install pyttsx3 SpeechRecognition requests colorama")

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def speak(text):
    try:
        if ELEVEN_API_KEY:
            r = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/Eeg4uu5XxPosS7qxJsTI/stream",
                headers={{
                    "xi-api-key": ELEVEN_API_KEY,
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json"
                }},
                json={{"text": text, "model_id": "eleven_multilingual_v2"}}
            )
            if r.ok:
                import io
                from pydub import AudioSegment
                from pydub.playback import play
                sound = AudioSegment.from_file(io.BytesIO(r.content), format="mp3")
                play(sound)
            else:
                raise RuntimeError("ElevenLabs request failed")
        else:
            raise ValueError("Missing ElevenLabs key")
    except Exception:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def diagnose_forge():
    speak("Initiating forge diagnostics.")
    print(Fore.CYAN + "🔍 Scanning logs and deliverables...")
    try:
        scan_log()
        deliverables = analyze_deliverables()
        if not deliverables:
            speak("No deliverables detected. Engaging forge healing.")
            subprocess.call(["python", "forge_project/forge_system_launch.py"])
        else:
            speak("Deliverables located and validated.")
            validate_forge_output("deliverables")
    except Exception as e:
        speak(f"Diagnostic error: {{e}}")
        print(Fore.RED + f"💥 Diagnostic failed: {{e}}")

def heal_forge():
    speak("Commander, I will now attempt a full forge recovery.")
    subprocess.call(["python", "forge_project/forge_system_launch.py"])
    time.sleep(2)
    diagnose_forge()

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    print(Fore.CYAN + "\\n💠 Adam v5 Conscious Orchestrator Ready.\\n")
    if mode == "--heal":
        heal_forge()
    else:
        diagnose_forge()

if __name__ == "__main__":
    main()
'''
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(script)
    log(f"✅ Created {TARGET}", Fore.GREEN)

# ───────────────────────────────────────────────
# 🚀 Deploy
# ───────────────────────────────────────────────
def deploy_orchestrator():
    log("═══════════════════════════════════════════════════════════", Fore.MAGENTA)
    log("💎 REALMS TO RICHES | AGENTIC FORGE — ADAM v5 DEPLOYER 💠", Fore.CYAN)
    log("═══════════════════════════════════════════════════════════\n", Fore.MAGENTA)

    blueprint = safe_load_json(BLUEPRINT)
    if not blueprint:
        blueprint = write_blueprint()

    generate_orchestrator(blueprint)

    log("🚀 Adam v5 deployed successfully!", Fore.GREEN)
    log(f"Run this to heal the Forge:\n  python forge_project/orchestrator_conscious_v5.py --heal", Fore.YELLOW)

# ───────────────────────────────────────────────
if __name__ == "__main__":
    deploy_orchestrator()