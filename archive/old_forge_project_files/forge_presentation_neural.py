#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
💎 Realms to Riches | Agentic Master Forge™ 2025 Robert Demotto Jr
FORGE PRESENTATION NEURAL — Cinematic Launch (System Player Edition)
─────────────────────────────────────────────────────────────
✅ Real-time ElevenLabs narration
✅ Rocket video cinematic via system player (no MoviePy)
✅ Auto summary + deliverable narration
✅ Safe UTF-8 output
─────────────────────────────────────────────────────────────
"""

import os, json, time, hashlib, warnings, requests, sys, threading, subprocess, platform
from datetime import datetime
from glob import glob
from colorama import init, Fore, Style
from pydub import AudioSegment
from pydub.playback import play

# ─────────────────────────────────────────────
# 🌐 Environment Setup
# ─────────────────────────────────────────────
warnings.filterwarnings("ignore")
init(autoreset=True)

if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

ASSETS = "assets/voices"
DELIVERABLES = "deliverables"
VIDEO_PATH = os.path.join("assets", "rocket_launch.mp4")

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
# 🔊 ElevenLabs Narration Utility
# ─────────────────────────────────────────────
def speak(agent, text, pause_after=0.8):
    """Generate, cache, and play speech for a given agent."""
    voice_id = VOICE_IDS.get(agent, VOICE_IDS["Adam"])
    hashed = hashlib.md5(text.encode()).hexdigest()[:8]
    base = os.path.join(ASSETS, f"{agent.lower()}_{hashed}")
    wav_file = f"{base}.wav"
    mp3_file = f"{base}.mp3"

    try:
        if ELEVEN_API_KEY and not os.path.exists(wav_file):
            headers = {
                "xi-api-key": ELEVEN_API_KEY,
                "Accept": "audio/mpeg",
                "Content-Type": "application/json"
            }
            payload = {"text": text, "model_id": "eleven_multilingual_v2"}
            r = requests.post(ELEVEN_URL.format(voice_id=voice_id),
                              headers=headers, json=payload, stream=True, timeout=20)
            if r.ok:
                with open(mp3_file, "wb") as f:
                    for chunk in r.iter_content(4096):
                        f.write(chunk)
                AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")
                os.remove(mp3_file)

        if os.path.exists(wav_file):
            play(AudioSegment.from_wav(wav_file))
        else:
            print(Fore.YELLOW + f"⚠️ Missing cached voice for {agent}")
        time.sleep(pause_after)
    except Exception as e:
        print(Fore.YELLOW + f"⚠️ Voice playback skipped ({agent}): {e}")

# ─────────────────────────────────────────────
# 🧩 Holographic Banner
# ─────────────────────────────────────────────
def holographic_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
{Fore.MAGENTA}{Style.BRIGHT}
╔════════════════════════════════════════════════════╗
║         💎 REALMS TO RICHES | AGENTIC FORGE™        ║
╚════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    speak("Adam", "Initializing Realms to Riches Forge Neural Presentation.")
    print(Fore.CYAN + "🚀 Neural Forge Presentation Sequence Engaged...\n")

# ─────────────────────────────────────────────
# 🎬 Cinematic Video Playback (System Default)
# ─────────────────────────────────────────────
def play_cinematic(video_path=VIDEO_PATH):
    """Play the rocket launch cinematic using the system's default video player."""
    if not os.path.exists(video_path):
        print(Fore.YELLOW + f"⚠️ Rocket cinematic not found: {video_path}")
        return

    print(Fore.CYAN + "🎞 Launching Forge cinematic window...")
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["start", "", video_path], shell=True)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", video_path])
        else:
            subprocess.Popen(["xdg-open", video_path])
    except Exception as e:
        print(Fore.RED + f"💥 Cinematic playback error: {e}")

# ─────────────────────────────────────────────
# 🔍 Deliverable Analysis
# ─────────────────────────────────────────────
def analyze_deliverables():
    md_files = glob(os.path.join(DELIVERABLES, "*.md"))
    summary = []
    for path in md_files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        code_blocks = text.count("```")
        snippet = " ".join(text.split()[:40]) + "..." if len(text) > 200 else text
        summary.append({
            "file": os.path.basename(path),
            "length": len(text),
            "code_blocks": code_blocks,
            "snippet": snippet
        })

    manifest = os.path.join(DELIVERABLES, "holo_manifest.json")
    json.dump(summary, open(manifest, "w"), indent=2)
    return summary

# ─────────────────────────────────────────────
# 🗣️ Narration and Summary
# ─────────────────────────────────────────────
def narrate_summary(summary):
    total = len(summary)
    speak("Elli", f"The Forge has successfully produced {total} deliverables.")
    for s in summary:
        speak("Charlotte", f"Deliverable {s['file']} analyzed. Contains approximately {s['length']} characters.")
    speak("Roger", "All assets verified. Preparing summary report.")

    report_path = os.path.join(DELIVERABLES, "FORGE_SUMMARY_REPORT.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🧩 Realms to Riches | Forge Summary Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        for s in summary:
            f.write(f"### {s['file']}\n- Length: {s['length']}\n- Code Blocks: {s['code_blocks']}\n- Snippet: {s['snippet']}\n\n")
    print(Fore.GREEN + f"\n📘 Summary written → {report_path}")

# ─────────────────────────────────────────────
# 🚀 Main Execution Flow
# ─────────────────────────────────────────────
def main():
    holographic_banner()

    # Run cinematic in parallel thread while narration begins
    cinematic_thread = threading.Thread(target=play_cinematic, daemon=True)
    cinematic_thread.start()

    speak("Charlotte", "Commencing analysis of the extracted forge deliverables.")
    summary = analyze_deliverables()
    if not summary:
        speak("Roger", "No deliverables detected. Presentation concluded.")
        return

    narrate_summary(summary)
    speak("Adam", "Neural Forge cinematic presentation complete. Awaiting further instruction.")
    print(Fore.CYAN + "\n🌐 REALMS TO RICHES PRESENTATION COMPLETE — Neural Intelligence Activated.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nPresentation interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"💥 Presentation error: {e}")
