import os
import time
import subprocess
import re
import json
from datetime import datetime

class GenesisForgeRunner:
    def __init__(self):
        self.max_requests_burst = 600    # 600 requests per minute
        self.max_requests_hour = 6000    # 6000 requests per hour  
        self.burst_timeout = 20          # 20 second timeout
        self.hour_timeout = 60           # 1 minute timeout
        self.completed_tasks = set()
        self.deliverables_dir = "genesis_forge_outputs"
        
    def extract_completed_tasks(self, output):
        """Extract and save completed task deliverables"""
        task_patterns = {
            'code_specification': r'## THE CODE.*?(?=##|\Z)',
            'compiler_architecture': r'## COMPILER ARCHITECTURE.*?(?=##|\Z)', 
            'agent_forge_system': r'## AGENT FORGE.*?(?=##|\Z)',
            'security_review': r'## SECURITY.*?(?=##|\Z)',
            'agent_identities': r'## AGENT IDENTIT.*?(?=##|\Z)',
            'ar_vr_environment': r'## AR.*VR.*HIL.*?(?=##|\Z)',
            'deployment_package': r'## DEPLOYMENT.*?(?=##|\Z)',
            'portability_docs': r'## PORTABILITY.*?(?=##|\Z)',
            'system_diagnosis': r'## DIAGNOS.*?(?=##|\Z)',
            'code_fixes': r'## FIX.*?(?=##|\Z)'
        }
        
        saved_tasks = []
        for task_name, pattern in task_patterns.items():
            matches = re.findall(pattern, output, re.DOTALL | re.IGNORECASE)
            if matches and len(matches[0]) > 200:  # Substantial content
                filepath = f"{self.deliverables_dir}/deliverable_{task_name}.txt"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(matches[0])
                saved_tasks.append(task_name)
                self.completed_tasks.add(task_name)
                print(f"✅ SAVED: {task_name} ({len(matches[0])} chars)")
        
        return saved_tasks
    
    def run_with_rate_limiting(self):
        """Run Genesis Forge with intelligent rate limiting"""
        os.makedirs(self.deliverables_dir, exist_ok=True)
        
        print("🚀 GENESIS FORGE RATE-LIMITED RUNNER")
        print("📊 Limits: 600/min burst, 6000/hour, smart timeouts")
        print("💾 Incremental deliverable saving enabled")
        print("=" * 50)
        
        attempt = 1
        while len(self.completed_tasks) < 10:  # Assuming 10 total tasks
            print(f"\n🔄 ATTEMPT {attempt} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"📋 Completed tasks: {len(self.completed_tasks)}/10")
            
            # Run crewai with live output
            process = subprocess.Popen(
                ['crewai', 'run'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            output_buffer = ""
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())  # Live terminal output
                    output_buffer += output
                    
                    # Check for completed tasks in real-time
                    if "Task completed" in output or "Final Answer" in output:
                        saved = self.extract_completed_tasks(output_buffer)
                        if saved:
                            print(f"💾 Saved {len(saved)} new deliverables")
            
            # Final extraction from full output
            final_saved = self.extract_completed_tasks(output_buffer)
            
            # Save full log
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f"{self.deliverables_dir}/full_log_{timestamp}.txt", 'w', encoding='utf-8') as f:
                f.write(output_buffer)
            
            # Check if rate limited
            if "429" in output_buffer or "rate_limit_exceeded" in output_buffer:
                if attempt % 3 == 0:  # Every 3rd attempt, use hour timeout
                    print(f"⏳ HOUR LIMIT - Waiting {self.hour_timeout}s...")
                    time.sleep(self.hour_timeout)
                else:
                    print(f"⏳ BURST LIMIT - Waiting {self.burst_timeout}s...")
                    time.sleep(self.burst_timeout)
            elif process.returncode == 0:
                print("✅ Genesis Forge completed successfully!")
                break
            else:
                print(f"❌ Non-rate-limit error (exit code: {process.returncode})")
                break
                
            attempt += 1
            
        print(f"\n🎯 FINAL STATUS: {len(self.completed_tasks)} tasks completed")
        print("📁 Check genesis_forge_outputs/ for all deliverables")

if __name__ == "__main__":
    runner = GenesisForgeRunner()
    runner.run_with_rate_limiting()
