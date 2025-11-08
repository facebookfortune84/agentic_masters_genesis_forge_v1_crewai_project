#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ 2025 Robert Demotto Jr
FORGE SYSTEM LAUNCH — Cinematic Neural Orchestration
───────────────────────────────────────────────────────────────
✅ Rebuilds manifest if missing
✅ Launches forge_master_runner + forge_presentation_neural with sync
✅ Cinematic terminal + ElevenLabs narration
✅ Logs full launch telemetry
───────────────────────────────────────────────────────────────
"""

import os, json, subprocess, time, threading, sys
from datetime import datetime
from colorama import Fore, Style, init
from pydub import AudioSegment
from pydub.playback import play
import requests, hashlib

if sys.platform.startswith("win"):
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

init(autoreset=True)

# ─────────────────────────────────────────────
# 🔧 CONFIGURATION
# ─────────────────────────────────────────────
ROOT = os.getcwd()
FORGE_DIR = os.path.join(ROOT, "forge_project")
DELIVERABLES = os.path.join(ROOT, "deliverables")
ASSETS = os.path.join(ROOT, "assets", "voices")
LOG = os.path.join(ROOT, "system_launch.log")

MASTER_RUNNER = os.path.join(FORGE_DIR, "forge_master_runner.py")
PRESENTATION = os.path.join(FORGE_DIR, "forge_presentation_neural.py")

os.makedirs(ASSETS, exist_ok=True)
os.makedirs(DELIVERABLES, exist_ok=True)

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

VOICE_IDS = {
    "Adam": "Eeg4uu5XxPosS7qxJsTI",
    "Elli": "jAiFFKFYK8uW3TnWlXah",
    "Charlotte": "BrOny4Lkm3SsSmSNv8hv",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17"
}

# ─────────────────────────────────────────────
# 🎧 Narration Utility
# ─────────────────────────────────────────────
def speak(agent, text, pause=0.6):
    voice_id = VOICE_IDS.get(agent, VOICE_IDS["Adam"])
    hash_id = hashlib.md5(text.encode()).hexdigest()[:8]
    base = os.path.join(ASSETS, f"{agent.lower()}_{hash_id}")
    wav_file, mp3_file = f"{base}.wav", f"{base}.mp3"

    try:
        if ELEVEN_API_KEY and not os.path.exists(wav_file):
            headers = {"xi-api-key": ELEVEN_API_KEY, "Accept": "audio/mpeg", "Content-Type": "application/json"}
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL.format(voice_id=voice_id), headers=headers, json=payload, stream=True, timeout=15)
            if r.ok:
                with open(mp3_file, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                os.remove(mp3_file)
        if os.path.exists(wav_file):
            play(AudioSegment.from_wav(wav_file))
        time.sleep(pause)
    except Exception as e:
        print(Fore.YELLOW + f"⚠️ Voice synthesis skipped ({agent}): {e}")

# ─────────────────────────────────────────────
# 🧾 LOGGING
# ─────────────────────────────────────────────
def log(msg, color=Fore.CYAN, style=Style.NORMAL):
    print(color + style + msg + Style.RESET_ALL)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")

def divider():
    log("="*70, Fore.MAGENTA)

# ─────────────────────────────────────────────
# 🔍 VERIFY MANIFEST
# ─────────────────────────────────────────────
def verify_manifest():
    path = os.path.join(DELIVERABLES, "holo_manifest.json")
    if os.path.exists(path):
        try:
            data = json.load(open(path))
            if data: return data
        except Exception: pass
    files = [f for f in os.listdir(DELIVERABLES) if f.endswith(".md")]
    data = [{"file": f, "length": os.path.getsize(os.path.join(DELIVERABLES, f))} for f in files]
    json.dump(data, open(path, "w"), indent=2)
    return data

# ─────────────────────────────────────────────
# 🧠 ENVIRONMENT VALIDATION
# ─────────────────────────────────────────────
def verify_environment():
    divider()
    log("🔍 Validating Neural Forge Environment...")
    if not os.getenv("ELEVENLABS_API_KEY"):
        log("⚠️ ELEVENLABS_API_KEY missing in environment.", Fore.YELLOW)
    else:
        log("✅ ElevenLabs API key detected.", Fore.GREEN)
    os.makedirs(DELIVERABLES, exist_ok=True)
    divider()
    speak("Roger", "Neural Forge environment verified and ready.")

# ─────────────────────────────────────────────
# 🚀 LAUNCH SEQUENCE
# ─────────────────────────────────────────────
def run_master():
    divider(); log("🚀 Launching Forge Master Runner...", Fore.YELLOW)
    speak("Adam", "Initializing Forge synthesis cycle.")
    subprocess.call(["python", MASTER_RUNNER])

def run_presentation():
    divider(); log("🎬 Launching Neural Presentation Sequence...", Fore.CYAN)
    speak("Charlotte", "Neural Presentation sequence now beginning.")
    try:
        subprocess.call(["python", PRESENTATION])
    except Exception as e:
        log(f"⚠️ Presentation launch failed: {e}", Fore.YELLOW)
        fallback = os.path.join("assets", "rocket_launch.mp4")
        if os.path.exists(fallback):
            log("🎞️  Fallback: Playing rocket video directly...", Fore.CYAN)
            from forge_presentation_neural import play_cinematic
            play_cinematic(fallback)
        else:
            log("⚠️ No cinematic available for fallback.", Fore.YELLOW)

def finalize():
    divider()
    data = verify_manifest()
    deliverable_count = len(data)
    log(f"📦 {deliverable_count} deliverables catalogued.", Fore.CYAN)
    if deliverable_count == 0:
        speak("Elli", "No deliverables were found. System integrity under review.")
    else:
        speak("Elli", f"{deliverable_count} verified deliverables confirmed.")
    divider()
    log("🌟 FORGE SYSTEM COMPLETE — Neural Broadcast Delivered.", Fore.GREEN)
    speak("Adam", "Realms to Riches Forge complete. Public neural relay broadcast initialized.")
    print(Fore.CYAN + "\nVisit: https://www.realmstoriches.xyz | © 2025 Robert Demotto Jr\n")

# ─────────────────────────────────────────────
# 🧠 MAIN ENTRY
# ─────────────────────────────────────────────
def main():
    divider()
    log("🌐 Neural Forge System Launch Initiated...", Fore.CYAN, Style.BRIGHT)
    speak("Adam", "Commencing Realms to Riches neural system activation sequence.")
    verify_environment()
    run_master()
    finalize()
    run_presentation()

if __name__ == "__main__":
    main()