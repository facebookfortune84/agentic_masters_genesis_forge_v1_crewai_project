import subprocess
import os

print("🚀 Launching Forge Master Runner…")

runner_path = os.path.join("forge project", "forge_master_runner.py")

if not os.path.exists(runner_path):
    print(f"❌ Could not find runner at: {runner_path}")
else:
    subprocess.call(["python", runner_path])