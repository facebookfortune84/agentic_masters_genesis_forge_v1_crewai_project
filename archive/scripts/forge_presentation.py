#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎬 Neural Forge Cinematic Presentation — ElevenLabs v2 API
"""
import os, shutil, zipfile, time, warnings
from colorama import Fore, Style, init
from datetime import datetime
init(autoreset=True)
warnings.filterwarnings("ignore")

def log(msg, color=Fore.CYAN): print(color + msg + Style.RESET_ALL)

# ── Extract latest forge to F:\ ───────────────────────────────────
def extract_latest_forge():
    zips = sorted([f for f in os.listdir('.') if f.startswith('RealmsToRiches_Forge_') and f.endswith('.zip')],
                  key=os.path.getmtime, reverse=True)
    if not zips: 
        log("⚠️ No Forge archive found."); return None
    latest=zips[0]; dest="F:\\"
    with zipfile.ZipFile(latest,'r') as zf:
        target=os.path.join(dest,latest.replace('.zip',''))
        os.makedirs(target,exist_ok=True); zf.extractall(target)
        log(f"📦 Extracted Forge to {target}", Fore.GREEN)
        return target

# ── ElevenLabs v2 Narration ──────────────────────────────────────
def narrate():
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play
        client=ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY",
            "sk_efad95d86d97598e0b17a5975febe8079859c7527af7a33a"))
        text=("Behold the Realms to Riches — Agentic Master Forge 2025. "
              "Forged by Robert Demotto Junior. All systems verified. "
              "Reality compilation complete.")
        audio=client.text_to_speech.convert(
            voice_id="Eeg4uu5XxPosS7qxJsTI", model_id="eleven_multilingual_v2",
            text=text, output_format="mp3_44100_128")
        play(audio)
    except Exception as e:
        log(f"⚠️ Narration skipped ({e})", Fore.YELLOW)

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    log("🎥 Cinematic Presentation Initiated", Fore.MAGENTA)
    target=extract_latest_forge()
    narrate()
    log("✅ Forge presentation complete", Fore.CYAN)
    log("🔗 Experience ElevenLabs voices → https://elevenlabs.io/app/voice-lab?action=create&aff=robertdemottojr",
        Fore.YELLOW)
    time.sleep(5)

if __name__=="__main__":
    main()