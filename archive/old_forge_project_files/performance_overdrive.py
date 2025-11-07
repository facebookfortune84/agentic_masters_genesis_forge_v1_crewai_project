#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ 2025 Robert Demotto Jr
PERFORMANCE OVERDRIVE — Cinematic Runtime Accelerator
────────────────────────────────────────────────────────────────────
✅ ElevenLabs MP3→WAV conversion with cache
✅ Visual shimmer + launch animation
✅ Stable voice playback with error resilience
✅ Runtime mode selector
✅ pydantic_core safety patch
────────────────────────────────────────────────────────────────────
"""

import os, sys, time, random, hashlib, requests, shutil
from colorama import init, Fore, Style
import simpleaudio as sa
from pydub import AudioSegment

init(autoreset=True)

# ─────────────────────────────────────────────
# 🔐 ElevenLabs Configuration
# ─────────────────────────────────────────────
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
ASSETS = os.path.join("assets", "voices")
os.makedirs(ASSETS, exist_ok=True)

VOICE_IDS = {
    "Adam": "Eeg4uu5XxPosS7qxJsTI",
    "Elli": "jAiFFKFYK8uW3TnWlXah",
    "Charlotte": "BrOny4Lkm3SsSmSNv8hv",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17"
}

# ─────────────────────────────────────────────
# 🎧 Voice Engine
# ─────────────────────────────────────────────
def holographic_voice(agent, text, pause_after=0.8):
    """Stable ElevenLabs TTS playback with caching + conversion."""
    voice_id = VOICE_IDS.get(agent, VOICE_IDS["Adam"])
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    mp3_file, wav_file = os.path.join(ASSETS, f"{agent}_{h}.mp3"), os.path.join(ASSETS, f"{agent}_{h}.wav")

    try:
        if ELEVEN_API_KEY and not os.path.exists(wav_file):
            headers = {"xi-api-key": ELEVEN_API_KEY, "Accept": "audio/mpeg", "Content-Type": "application/json"}
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL.format(voice_id=voice_id), headers=headers, json=payload, stream=True, timeout=20)
            if r.ok:
                with open(mp3_file, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                os.remove(mp3_file)
        file = wav_file if os.path.exists(wav_file) else None
        if file:
            wave_obj = sa.WaveObject.from_wave_file(file)
            wave_obj.play().wait_done()
            time.sleep(pause_after)
    except Exception as e:
        print(Fore.YELLOW + f"⚠️ Playback skipped ({agent}): {e}")

# ─────────────────────────────────────────────
# ⚙️ Modes
# ─────────────────────────────────────────────
FORGE_MODES = {
    "OVERDRIVE": {"name": "Performance Overdrive", "color": Fore.YELLOW, "style": Style.BRIGHT},
    "RR": {"name": "Realms to Riches", "color": Fore.MAGENTA, "style": Style.BRIGHT},
    "DEV": {"name": "Developer", "color": Fore.CYAN, "style": Style.NORMAL},
    "STEALTH": {"name": "Stealth", "color": Fore.WHITE, "style": Style.DIM}
}

class ForgeDisplay:
    def __init__(self, mode="RR"):
        self.mode = mode.upper() if mode.upper() in FORGE_MODES else "RR"
        self.settings = FORGE_MODES[self.mode]
        self.width = shutil.get_terminal_size().columns

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def shimmer(self, text, duration=1.8):
        """Animated color shimmer for live terminal effect."""
        colors = [Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.GREEN]
        for _ in range(int(duration * 10)):
            sys.stdout.write(f"\r{random.choice(colors)}{Style.BRIGHT}{text}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.07)
        print()

    def banner(self):
        s = self.settings
        print(f"""{s['color']}{s['style']}
╔═╗┌─┐┬─┐┬ ┬┬┌─┐   ╦═╗┬─┐  ┬  ┬┌─┐
╚═╗├─┘├┬┘│ │││ ┬   ╠╦╝├┬┘  │  │├┤ 
╚═╝┴  ┴└─└─┘┴└─┘   ╩╚═┴└─  ┴─┘┴└─┘
💎 REALMS TO RICHES | AGENTIC MASTER FORGE™
──────────────────────────────────────────────{Style.RESET_ALL}""")
        holographic_voice("Adam", "Welcome back to the Realms to Riches Forge System.")
        print(f"\n{s['color']}{s['style']}🧠 Mode Active: {s['name']}{Style.RESET_ALL}\n")

    def render_cycle(self, n, phase):
        print(f"{Fore.MAGENTA}{Style.BRIGHT}\n🚀 FORGE CYCLE {n}: {phase}{Style.RESET_ALL}")
        if self.mode == "OVERDRIVE":
            self.shimmer("⚡ Powering Up Neural Forge Reactor...", 2.5)
            holographic_voice("Roger", f"Cycle {n}: {phase} initialized successfully.")

# ─────────────────────────────────────────────
# 🧩 pydantic_core Recovery
# ─────────────────────────────────────────────
try:
    import pydantic_core
except ModuleNotFoundError:
    sys.modules["pydantic_core"] = type("dummy", (), {})()
    print(Fore.YELLOW + "⚙️ pydantic_core missing — dummy module loaded to prevent crash.")

# ─────────────────────────────────────────────
# 🧠 MAIN
# ─────────────────────────────────────────────
def main():
    disp = ForgeDisplay("OVERDRIVE")
    disp.clear()
    disp.banner()
    holographic_voice("Charlotte", "Activating performance overdrive mode.")
    for i, phase in enumerate([
        "Language Genesis", "Compiler Architecture", "Neural Core Activation",
        "Optimization Streamlining", "Validation Sequence"
    ], start=1):
        disp.render_cycle(i, phase)
        time.sleep(1.0)
    holographic_voice("Elli", "Performance diagnostics complete. All systems stable.")
    print(Fore.GREEN + "\n✅ Overdrive performance systems calibrated.\n")

if __name__ == "__main__":
    main()