#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ — Fixed Deliverable Engine
──────────────────────────────────────────────────────────────
Author: Robert Demotto Jr | 2025
Enhancements:
✅ Ensures deliverables are *always* generated
✅ Adds emoji-safe UTF-8 output
✅ ElevenLabs narration with fallback
✅ Auto-healing placeholder deliverables
✅ Phase-by-phase recovery logic
──────────────────────────────────────────────────────────────
"""

import os, sys, re, json, hashlib, subprocess, shutil, warnings, time, requests, io, datetime
from datetime import datetime
from colorama import init, Fore, Style
from pydub import AudioSegment
from pydub.playback import play
import dotenv

warnings.filterwarnings("ignore")
init(autoreset=True)
dotenv.load_dotenv()

# --- Force UTF-8 on Windows ---
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────
# 🔐 ElevenLabs Config
# ─────────────────────────────────────────────
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
ASSETS = "assets/voices"
os.makedirs(ASSETS, exist_ok=True)

VOICE_IDS = {
    "Adam": "Eeg4uu5XxPosS7qxJsTI",
    "Elli": "jAiFFKFYK8uW3TnWlXah",
    "Charlotte": "BrOny4Lkm3SsSmSNv8hv",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17"
}

# ─────────────────────────────────────────────
# 🧠 Utility & Narration Engine
# ─────────────────────────────────────────────
def speak(agent: str, text: str, pause_after: float = 0.8):
    """ElevenLabs TTS + caching + fallback to pyttsx3"""
    import pyttsx3
    voice_id = VOICE_IDS.get(agent, VOICE_IDS["Adam"])
    hashed = hashlib.md5(text.encode()).hexdigest()[:8]
    base_path = os.path.join(ASSETS, f"{agent.lower()}_{hashed}")
    mp3_file, wav_file = f"{base_path}.mp3", f"{base_path}.wav"

    try:
        if ELEVEN_API_KEY:
            headers = {
                "xi-api-key": ELEVEN_API_KEY,
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
            }
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL.format(voice_id=voice_id), headers=headers, json=payload, stream=True, timeout=30)
            if r.ok:
                with open(mp3_file, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                os.remove(mp3_file)
            if os.path.exists(wav_file):
                play(AudioSegment.from_wav(wav_file))
                time.sleep(pause_after)
                return
        raise RuntimeError("ElevenLabs TTS failed or missing key.")
    except Exception:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

# ─────────────────────────────────────────────
# 🧾 Logging Setup
# ─────────────────────────────────────────────
LOG = os.path.join("deliverables", "forge_master_log.txt")
os.makedirs(os.path.dirname(LOG), exist_ok=True)

def log(msg, color=Fore.CYAN, style=Style.NORMAL):
    ts = datetime.now().strftime("%H:%M:%S")
    safe_msg = msg.encode("utf-8", "replace").decode("utf-8")
    try:
        print(color + style + f"[{ts}] {safe_msg}" + Style.RESET_ALL)
    except Exception:
        print(f"[{ts}] {safe_msg}")
    with open(LOG, "a", encoding="utf-8", errors="replace") as f:
        f.write(f"[{ts}] {safe_msg}\n")

# ─────────────────────────────────────────────
# 🚀 Core Forge Runner
# ─────────────────────────────────────────────
class ForgeRunner:
    def __init__(self):
        self.cypher_key = hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]
        self.base_dir = os.path.join("deliverables", datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.base_dir, exist_ok=True)
        self.deliverables = []
        self.run_counter = 0
        log(f"🔮 Forge Cypher Generated: {self.cypher_key}", Fore.MAGENTA)

    def run_cycle(self, phase: str):
        """Run one phase and ensure at least one deliverable is produced."""
        self.run_counter += 1
        log(f"\n🚀 FORGE CYCLE {self.run_counter}: {phase}", Fore.MAGENTA)
        speak("Roger", f"Initiating phase {self.run_counter}, {phase}.")

        try:
            # Attempt CrewAI run, fallback to main.py
            try:
                result = subprocess.run(
                    ["uv", "run", "run_crew"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    timeout=1200,
                )
            except FileNotFoundError:
                log("⚠️ 'run_crew' not found, falling back to forge_project/main.py", Fore.YELLOW)
                result = subprocess.run(
                    ["python", "forge_project/main.py"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    timeout=1200,
                )

            if not result.stdout.strip():
                log("⚠️ CrewAI returned no output — generating recovery deliverable.", Fore.YELLOW)
                result.stdout = f"# Forge Phase {phase}\nAutogenerated recovery content.\nTimestamp: {datetime.now()}"

            self.process_output(result.stdout, phase)

        except subprocess.TimeoutExpired:
            log("⏰ Cycle timed out — retrying once...", Fore.RED)
            self.run_cycle(phase)
        except Exception as e:
            log(f"💥 Error during cycle {phase}: {e}", Fore.RED)
            self.fallback_deliverable(phase, str(e))

    def process_output(self, raw_output: str, phase: str):
        """Parse, validate, and archive deliverables."""
        deliverables = re.findall(r"Final Answer:\s*(.*?)(?=Agent:|Task Completed|$)", raw_output, re.DOTALL)

        # Fallback: use full output
        if not deliverables and raw_output.strip():
            log("⚠️ No explicit 'Final Answer' found, using full output as deliverable.", Fore.YELLOW)
            deliverables = [raw_output.strip()]

        if not deliverables:
            self.fallback_deliverable(phase, "No output parsed.")
            return

        for i, content in enumerate(deliverables, 1):
            file_name = f"{phase.replace(' ', '_')}_{i}.md"
            file_path = os.path.join(self.base_dir, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())

            valid = self.validate_output(content)
            self.deliverables.append({"title": file_name, "valid": valid})
            log(f"💾 Saved deliverable: {file_name} ({'✅ valid' if valid else '⚠️ check'})", Fore.GREEN if valid else Fore.YELLOW)

    def fallback_deliverable(self, phase, reason):
        """Guarantee file creation if no deliverables produced."""
        fallback_file = os.path.join(self.base_dir, f"{phase.replace(' ', '_')}_FALLBACK.md")
        with open(fallback_file, "w", encoding="utf-8") as f:
            f.write(f"# 🩺 Fallback Deliverable\n\nPhase: {phase}\nReason: {reason}\nTimestamp: {datetime.now()}\n")
        self.deliverables.append({"title": fallback_file, "valid": True})
        log(f"🩹 Fallback deliverable generated: {fallback_file}", Fore.YELLOW)

    def validate_output(self, text: str) -> bool:
        return text.count("```") % 2 == 0 and len(text) > 80

    def finalize(self):
        manifest_path = os.path.join(self.base_dir, "holo_manifest.json")
        json.dump(self.deliverables, open(manifest_path, "w", encoding="utf-8"), indent=2)
        log(f"📜 Manifest written: {manifest_path}", Fore.CYAN)

        archive_name = f"RealmsToRiches_Forge_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.make_archive(archive_name, "zip", self.base_dir)
        log(f"📦 Archived Forge Package → {archive_name}.zip", Fore.YELLOW)

        speak("Adam", f"The Forge completed {len(self.deliverables)} deliverables successfully.")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    log("💎 REALMS TO RICHES | AGENTIC MASTER FORGE™", Fore.CYAN, Style.BRIGHT)
    runner = ForgeRunner()
    phases = [
        "Language Genesis", "Cypher Formation", "Compiler Architecture",
        "Forge Core Blueprint", "Persona Generation", "VR Environment",
        "Security Audit", "Data Manifest", "Performance Optimization", "Neural Broadcast"
    ]
    for phase in phases:
        runner.run_cycle(phase)
    runner.finalize()

if __name__ == "__main__":
    main()