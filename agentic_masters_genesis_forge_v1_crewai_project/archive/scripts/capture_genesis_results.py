import os
import json
from datetime import datetime

# Create outputs directory
os.makedirs("genesis_forge_outputs", exist_ok=True)

print("=== RUNNING GENESIS FORGE WITH OUTPUT CAPTURE ===")
print("Starting crew execution...")

# Import and run the crew
import sys
sys.path.append("src")

from agentic_masters_genesis_forge.main import run

# Capture outputs
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

try:
    result = run({"project_type": "Genesis Forge", "iteration": timestamp})
    
    # Save result to file
    output_file = f"genesis_forge_outputs/execution_result_{timestamp}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== RESULTS SAVED TO: {output_file} ===")
    print("Genesis Forge execution completed successfully!")
    
    # Also save as text for readability
    text_file = f"genesis_forge_outputs/execution_result_{timestamp}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(str(result))
    
    print(f"Text version saved to: {text_file}")
    
except Exception as e:
    error_file = f"genesis_forge_outputs/error_log_{timestamp}.txt"
    with open(error_file, "w") as f:
        f.write(f"Error occurred: {str(e)}\n")
        f.write(f"Timestamp: {timestamp}\n")
    print(f"Error occurred. Details saved to: {error_file}")
    raise e

