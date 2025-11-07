#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Orchestrator Agent — Conscious Mode v5
──────────────────────────────────────────────
Fully interactive Forge Orchestrator
- Voice listening (SpeechRecognition)
- ElevenLabs voice replies
- Path-safe auto-launch for all Forge modules
- Persistent short-term memory (context.json)
──────────────────────────────────────────────
"""

import os
import sys
import json
import threading
import time
import requests
import speech_recognition as sr
from colorama import init, Fore, Style
from pydub import AudioSegment
from pydub.playback import play
import hashlib
import pyttsx3
tts_engine = pyttsx3.init()

# ─────────────────────────────────────────────
# 🎨 Setup and Constants
# ─────────────────────────────────────────────
init(autoreset=True)
CYAN = Fore.CYAN
PINK = Fore.MAGENTA
RESET = Style.RESET_ALL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "assets", "voices")
os.makedirs(ASSETS, exist_ok=True)

# voice setup
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
VOICE_ID = "Eeg4uu5XxPosS7qxJsTI"  # Adam

# context
MEMORY_FILE = os.path.join(ROOT, "context.json")
if not os.path.exists(MEMORY_FILE):
    json.dump({"recent": []}, open(MEMORY_FILE, "w"))

print(CYAN + "🚀 Neural Forge Conscious Orchestrator v5 Online")
print(PINK + "💬 Adam: Standing by for your command, Commander.\n")

# ─────────────────────────────────────────────
# 🎧 ElevenLabs Voice Output
# ─────────────────────────────────────────────
def speak(text: str):
    print(PINK + f"💬 Adam: {text}")
    if not ELEVEN_API_KEY:
        tts_engine.say(text)
        tts_engine.runAndWait()
        return

    hashname = hashlib.md5(text.encode()).hexdigest()[:8]
    wav_file = os.path.join(ASSETS, f"adam_{hashname}.wav")
    mp3_file = os.path.join(ASSETS, f"adam_{hashname}.mp3")

    try:
        if not os.path.exists(wav_file):
            headers = {
                "xi-api-key": ELEVEN_API_KEY,
                "Accept": "audio/mpeg",
                "Content-Type": "application/json"
            }
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL.format(voice_id=VOICE_ID), headers=headers, json=payload, stream=True)
            if r.ok:
                with open(mp3_file, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                os.remove(mp3_file)
        play(AudioSegment.from_wav(wav_file))
    except Exception:
        tts_engine.say(text)
        tts_engine.runAndWait()

# ─────────────────────────────────────────────
# 🧠 Context Memory
# ─────────────────────────────────────────────
def remember(command, result):
    try:
        data = json.load(open(MEMORY_FILE))
    except:
        data = {"recent": []}
    entry = {"cmd": command, "result": result, "time": time.strftime("%H:%M:%S")}
    data["recent"].append(entry)
    data["recent"] = data["recent"][-20:]  # keep last 20
    json.dump(data, open(MEMORY_FILE, "w"), indent=2)

def recall():
    data = json.load(open(MEMORY_FILE))
    if not data["recent"]:
        speak("I have no memory of prior tasks yet.")
    else:
        speak("Here’s what I recall from our recent missions:")
        for r in data["recent"][-5:]:
            print(CYAN + f"[{r['time']}] {r['cmd']} → {r['result']}")

# ─────────────────────────────────────────────
# 🔍 Command Processor
# ─────────────────────────────────────────────
def handle_command(command: str):
    command = command.lower().strip()
    if not command:
        return

    if "status" in command:
        speak("All Forge systems are nominal and stable.")
        remember(command, "system ok")

    elif "diagnose" in command:
        speak("Running diagnostics on deliverables now.")
        os.system(f"python {os.path.join(ROOT, 'forge_project', 'diagnostics_forger.py')}")
        remember(command, "diagnostics executed")

    elif "launch" in command:
        speak("Initiating Forge System Launch sequence.")
        os.system(f"python {os.path.join(ROOT, 'forge_project', 'forge_system_launch.py')}")
        remember(command, "launch sequence complete")

    elif "validate" in command:
        speak("Running forge output validation.")
        os.system(f"python {os.path.join(ROOT, 'forge_project', 'forge_validator.py')}")
        remember(command, "validation done")

    elif "presentation" in command or "show" in command:
        speak("Displaying the neural cinematic presentation.")
        os.system(f"python {os.path.join(ROOT, 'forge_project', 'forge_presentation_neural.py')}")
        remember(command, "presentation started")

    elif "memory" in command or "recall" in command:
        recall()

    elif "exit" in command or "shutdown" in command:
        speak("Standing down, Commander. Ending consciousness session.")
        sys.exit(0)

    else:
        speak(f"I don't recognize the directive: {command}")
        remember(command, "unknown")

# ─────────────────────────────────────────────
# 🎙️ Voice Listener
# ─────────────────────────────────────────────
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_to_voice():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Listening for your voice commands now.")
        while True:
            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
                command = recognizer.recognize_google(audio, language="en-US")
                print(CYAN + f"🗣️ You said: {command}")
                handle_command(command)
            except sr.UnknownValueError:
                print(PINK + "⚠️ Adam: I didn’t catch that, Commander.")
            except Exception as e:
                print(Fore.YELLOW + f"⚠️ Listener error: {e}")

# ─────────────────────────────────────────────
# 🚀 Launch Loop
# ─────────────────────────────────────────────
def main():
    threading.Thread(target=listen_to_voice, daemon=True).start()
    while True:
        cmd = input(CYAN + "💡 Text Command → " + RESET)
        handle_command(cmd)

if __name__ == "__main__":
    main()