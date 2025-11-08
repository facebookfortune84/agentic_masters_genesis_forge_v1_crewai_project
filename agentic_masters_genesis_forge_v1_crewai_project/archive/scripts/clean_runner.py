import subprocess
import time
import os
from datetime import datetime

def run_clean():
    print("🚀 GENESIS FORGE - CLEAN MODE")
    print("===============================")
    
    os.makedirs("outputs", exist_ok=True)
    
    for attempt in range(1, 4):  # Just 3 attempts max
        timestamp = datetime.now().strftime('%H%M%S')
        print(f"\n🔄 Attempt {attempt}/3 - {datetime.now().strftime('%H:%M:%S')}")
        
        # Set environment to fix encoding issues
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        # Run with minimal output
        try:
            result = subprocess.run(
                ['uv', 'run', 'run_crew'], 
                capture_output=True, 
                text=True, 
                timeout=300,  # 5 min timeout
                env=env,
                encoding='utf-8',
                errors='ignore'
            )
            
            # Save full output to file
            output_file = f"outputs/attempt_{attempt}_{timestamp}.log"
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(f"Return Code: {result.returncode}\n")
                f.write(f"STDOUT:\n{result.stdout}\n")
                f.write(f"STDERR:\n{result.stderr}\n")
            
            print(f"📁 Saved: {output_file}")
            
            # Simple status check
            if result.returncode == 0:
                print("✅ SUCCESS! Check output file for results.")
                break
            elif "429" in str(result.stderr) or "rate_limit" in str(result.stderr):
                print("⏳ Rate limited - waiting 2 minutes...")
                time.sleep(120)  # 2 min wait
            else:
                print(f"❌ Failed with code: {result.returncode}")
                print("Check output file for details.")
                break
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout after 5 minutes")
            break
        except Exception as e:
            print(f"💥 Error: {e}")
            break
    
    print("\n🏁 DONE! Check 'outputs' folder for all logs.")

if __name__ == "__main__":
    run_clean()
