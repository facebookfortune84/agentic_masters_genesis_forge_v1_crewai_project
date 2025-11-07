#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💠 Adam v5 — Conscious Orchestrator
────────────────────────────────────────────
Role: Autonomous Forge Coordinator
Modes: diagnostic, forge_healing, conversation, training
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
                headers={
                    "xi-api-key": ELEVEN_API_KEY,
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json"
                },
                json={"text": text, "model_id": "eleven_multilingual_v2"}
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
        speak(f"Diagnostic error: {e}")
        print(Fore.RED + f"💥 Diagnostic failed: {e}")

def heal_forge():
    speak("Commander, I will now attempt a full forge recovery.")
    subprocess.call(["python", "forge_project/forge_system_launch.py"])
    time.sleep(2)
    diagnose_forge()

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else None
    print(Fore.CYAN + "\n💠 Adam v5 Conscious Orchestrator Ready.\n")
    if mode == "--heal":
        heal_forge()
    else:
        diagnose_forge()

if __name__ == "__main__":
    main()
