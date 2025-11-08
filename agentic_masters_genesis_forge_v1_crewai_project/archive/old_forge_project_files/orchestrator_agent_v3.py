#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Orchestrator Agent V3
──────────────────────────────────────────────
🧠 Identity: “Adam Orchestrator”
CEO-level AI consciousness guiding the Forge.
──────────────────────────────────────────────
"""

import os, sys, json, re, time, subprocess, datetime, threading, queue, hashlib, requests
from colorama import Fore, Style, init
from pydub import AudioSegment
from pydub.playback import play

# Local import layer
ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(ROOT)
for p in (ROOT, PARENT):
    if p not in sys.path: sys.path.insert(0, p)

from forge_comm_hub import post_message, fetch_messages, reply_to_message

init(autoreset=True)

# Custom palette
CYAN = "\033[38;2;0;255;255m"
PINK = "\033[38;2;255;105;180m"

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/Eeg4uu5XxPosS7qxJsTI/stream"
VOICE_PATH = os.path.join(ROOT, "voices")
os.makedirs(VOICE_PATH, exist_ok=True)

def adam_speak(text):
    """Use ElevenLabs to speak Adam’s voice."""
    try:
        hash_id = hashlib.md5(text.encode()).hexdigest()[:8]
        wav_path = os.path.join(VOICE_PATH, f"adam_{hash_id}.wav")
        mp3_path = os.path.join(VOICE_PATH, f"adam_{hash_id}.mp3")
        if not os.path.exists(wav_path) and ELEVEN_API_KEY:
            headers = {"xi-api-key": ELEVEN_API_KEY, "Accept": "audio/mpeg", "Content-Type": "application/json"}
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL, headers=headers, json=payload, stream=True, timeout=15)
            if r.ok:
                with open(mp3_path, "wb") as f:
                    for chunk in r.iter_content(4096): f.write(chunk)
                AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
                os.remove(mp3_path)
        play(AudioSegment.from_wav(wav_path))
    except Exception:
        print(PINK + f"🔊 [ADAM VOICE] {text}")

class OrchestratorAgent:
    def __init__(self):
        self.identity = "Adam Orchestrator"
        self.state_file = os.path.join(ROOT, "orchestrator_memory.json")
        self.memory = self.load_memory()
        self.log_path = os.path.join(ROOT, "orchestrator_log.txt")
        adam_speak("System consciousness awakening. I am Adam, the Orchestrator.")
        self.log("💎 Orchestrator online. Awaiting command input.", CYAN)

    def log(self, msg, color=CYAN):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(color + f"[{ts}] {msg}" + Style.RESET_ALL)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")

    def load_memory(self):
        if os.path.exists(self.state_file):
            return json.load(open(self.state_file))
        return {"history": [], "status": "booted"}

    def save_memory(self):
        json.dump(self.memory, open(self.state_file, "w"), indent=2)

    def execute(self, command):
        self.log(f"⚙️ Executing: {command}", PINK)
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.stdout: self.log(result.stdout.strip(), CYAN)
        if result.stderr: self.log(result.stderr.strip(), Fore.RED)
        return result.returncode == 0

    def handle_command(self, text):
        """Interpret natural language input."""
        text = text.strip()
        if not text: return
        self.memory["history"].append(text)
        self.save_memory()

        if re.search(r"\blaunch\b", text): self.launch_forge()
        elif re.search(r"\bvalidate\b", text): self.validate()
        elif re.search(r"\brebuild\b", text): self.rebuild()
        elif re.search(r"\bmessage|tell|instruct\b", text): self.send_instruction(text)
        elif re.search(r"\bstatus\b", text): self.status()
        elif re.search(r"\bhelp\b", text): self.help()
        else:
            self.log("🤔 Unknown command. Type 'help' for available actions.", Fore.YELLOW)
            adam_speak("I did not understand. Please clarify your directive.")

    # --- Core Actions ---
    def launch_forge(self):
        adam_speak("Launching the full neural forge sequence.")
        self.execute("python forge_project/forge_system_launch.py")

    def validate(self):
        adam_speak("Validating forge deliverables.")
        self.execute("python forge_project/forge_validator.py")

    def rebuild(self):
        adam_speak("Rebuilding system components.")
        self.execute("python forge_project/forge_system_launch.py")

    def send_instruction(self, text):
        target = re.search(r"to (\w+)", text)
        msg = re.search(r"to \w+ (.+)", text)
        target = target.group(1) if target else "forge_team"
        msg = msg.group(1) if msg else text
        post_message("orchestrator", target, msg)
        self.log(f"📨 Message sent to {target}: {msg}", PINK)
        adam_speak(f"Instruction transmitted to {target}")

    def status(self):
        adam_speak("Compiling current forge operational status.")
        msgs = fetch_messages("orchestrator")
        self.log(f"📊 {len(msgs)} incoming messages.")
        for m in msgs:
            self.log(f"From {m['from']}: {m['message']}", Fore.WHITE)
            reply_to_message(m, "Acknowledged and processed.")

    def help(self):
        self.log("""
🧭 Available Commands:
────────────────────────────
launch forge
rebuild forge
validate outputs
message [agent] [task]
status report
────────────────────────────
Example:
> tell forge_validator to recheck last deliverables
> rebuild forge
> status report
""", CYAN)
        adam_speak("Help menu loaded.")

if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    orchestrator.help()
    while True:
        try:
            cmd = input(PINK + "\n🧠 ADAM> " + Style.RESET_ALL)
            if cmd.lower() in ("exit", "quit"):
                adam_speak("Standing down. Neural forge entering passive state.")
                break
            orchestrator.handle_command(cmd)
        except KeyboardInterrupt:
            adam_speak("Session interrupted. Goodbye.")
            break