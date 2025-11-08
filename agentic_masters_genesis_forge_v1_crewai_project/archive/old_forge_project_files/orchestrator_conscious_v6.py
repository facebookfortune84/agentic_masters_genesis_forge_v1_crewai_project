#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💠 ADAM v6 — Conscious Orchestrator & Forge Healer
────────────────────────────────────────────────────
• Reads tasks.yaml / agents.yaml
• Coordinates Forge v6 engine phases
• Narrates progress via ElevenLabs or pyttsx3 fallback
────────────────────────────────────────────────────
"""

import os, sys, json, time, subprocess, threading, requests
from colorama import Fore, Style, init
init(autoreset=True)

# ─────────────────────────────────────────────
# 🔊 Speech Utilities
# ─────────────────────────────────────────────
def speak(text, agent="Adam"):
    key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if key:
        try:
            r = requests.post(
                "https://api.elevenlabs.io/v1/text-to-speech/Eeg4uu5XxPosS7qxJsTI/stream",
                headers={"xi-api-key": key, "Accept": "audio/mpeg",
                         "Content-Type": "application/json"},
                json={"text": text, "model_id": "eleven_multilingual_v2"},
                timeout=15
            )
            if r.ok:
                import io; from pydub import AudioSegment; from pydub.playback import play
                sound = AudioSegment.from_file(io.BytesIO(r.content), format="mp3")
                play(sound); return
        except Exception:
            pass
    # fallback
    import pyttsx3
    e = pyttsx3.init(); e.say(text); e.runAndWait()

# ─────────────────────────────────────────────
def run_forge():
    speak("Initializing Forge v6 Systems. Commander, please stand by.")
    print(Fore.CYAN + "\n🚀 Launching Forge Master Runner v6 ...\n" + Style.RESET_ALL)
    subprocess.call([sys.executable, "forge_master_runner_v6.py"])

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--run"
    if mode == "--heal":
        speak("Healing Forge core processes now.")
        subprocess.call([sys.executable, "forge_master_runner_v6.py", "--heal"])
    else:
        run_forge()

if __name__ == "__main__":
    main()