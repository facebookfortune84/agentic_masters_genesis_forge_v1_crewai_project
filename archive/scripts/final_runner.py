import subprocess
import time
import os
import json
from datetime import datetime
import re

class OptimizedGenesisForgeCrew:
    def __init__(self):
        self.progress_file = 'genesis_progress.json'
        self.deliverables_dir = 'deliverables'
        
        # Your 10 Genesis Forge tasks
        self.completed_tasks = {
            'design_the_code_specification': False,
            'diagnose_system_error': False, 
            'design_the_code_compiler_architecture': False,
            'architect_agent_forge_core_system': False,
            'design_dsl_generator': False,
            'implement_memory_module_system': False,
            'build_security_framework': False,
            'create_documentation': False,
            'develop_test_suite': False,
            'generate_final_report': False
        }
        
        # Dev tier - much shorter delays!
        self.success_delay = 30    # 30s after success
        self.retry_delay = 60      # 1m after failure
        self.rate_limit_delay = 90 # 1.5m after rate limit (unlikely now!)
        
        os.makedirs(self.deliverables_dir, exist_ok=True)
        self.load_progress()
    
    def load_progress(self):
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                self.completed_tasks.update(data.get('completed_tasks', {}))
    
    def save_progress(self):
        data = {
            'completed_tasks': self.completed_tasks,
            'last_run': datetime.now().isoformat(),
            'total_completed': sum(self.completed_tasks.values())
        }
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def extract_deliverable(self, output_text, task_name):
        patterns = [
            r'Final Answer:\s*(.*?)(?=Agent:|Task Completed|┌|═|$)',
            r'Status: ✅ Completed.*?Final Answer:\s*(.*?)(?=┌|═|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, output_text, re.DOTALL | re.IGNORECASE)
            if matches:
                deliverable = matches[-1].strip()
                if deliverable and len(deliverable) > 150:
                    timestamp = datetime.now().strftime('%H%M%S')
                    filename = f"{self.deliverables_dir}/{task_name}_{timestamp}.md"
                    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(f"# {task_name.replace('_', ' ').title()}\n")
                        f.write(f"**Genesis Forge Project Deliverable**\n\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Task: {task_name}\n\n")
                        f.write("---\n\n")
                        f.write(deliverable)
                    print(f"💾 SAVED: {filename}")
                    return True
        return False
    
    def analyze_progress(self, output_text):
        """Enhanced progress analysis"""
        initial_completed = sum(self.completed_tasks.values())
        
        # Look for completed tasks
        completed_patterns = [
            r'Task: (\w+).*?Status: ✅ Completed',
            r'┌.*?Task Completed.*?Name: (\w+)',
            r'Task Completed.*?Name: (\w+)'
        ]
        
        for pattern in completed_patterns:
            matches = re.findall(pattern, output_text, re.DOTALL)
            for task_id in matches:
                if task_id in self.completed_tasks and not self.completed_tasks[task_id]:
                    print(f"✅ COMPLETED: {task_id}")
                    self.completed_tasks[task_id] = True
                    self.extract_deliverable(output_text, task_id)
        
        new_completed = sum(self.completed_tasks.values())
        return new_completed > initial_completed
    
    def show_dashboard(self):
        completed = sum(self.completed_tasks.values())
        total = len(self.completed_tasks)
        progress_bar = "█" * completed + "░" * (total - completed)
        
        print(f"\n🏗️  GENESIS FORGE PROJECT DASHBOARD")
        print(f"{'='*50}")
        print(f"Progress: [{progress_bar}] {completed}/{total} ({completed/total*100:.0f}%)")
        print(f"{'='*50}")
        
        for i, (task, done) in enumerate(self.completed_tasks.items(), 1):
            status = "✅" if done else "⏳" if i == completed + 1 else "⚪"
            name = task.replace('_', ' ').title()
            print(f"{i:2d}. {status} {name}")
        
        if completed < total:
            remaining = [k for k, v in self.completed_tasks.items() if not v]
            print(f"\n🎯 NEXT: {remaining[0].replace('_', ' ').title()}")
            print(f"📋 Remaining: {len(remaining)} tasks")
        else:
            print(f"\n🏆 PROJECT COMPLETE! All {total} tasks done!")
    
    def run_attempt(self, attempt):
        timestamp = datetime.now().strftime('%H%M%S')
        
        try:
            print(f"\n🚀 RUN #{attempt} - {datetime.now().strftime('%H:%M:%S')}")
            
            # Run with dev tier confidence
            result = subprocess.run(
                ['uv', 'run', 'run_crew'], 
                capture_output=True, 
                text=True, 
                timeout=1200,  # 20 min - longer for complex tasks
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'},
                encoding='utf-8',
                errors='ignore'
            )
            
            # Save detailed log
            log_file = f"outputs/dev_run_{attempt}_{timestamp}.log"
            with open(log_file, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(f"GENESIS FORGE - DEV TIER RUN #{attempt}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Return Code: {result.returncode}\n\n")
                f.write("STDOUT:\n")
                f.write("="*50 + "\n")
                f.write(result.stdout + "\n\n")
                f.write("STDERR:\n") 
                f.write("="*50 + "\n")
                f.write(result.stderr + "\n")
            
            print(f"📁 LOG: {log_file}")
            
            # Analyze what happened
            progress_made = False
            if result.stdout:
                progress_made = self.analyze_progress(result.stdout)
                self.save_progress()
            
            # Determine next action
            if "rate_limit" in str(result.stderr):
                print(f"⏳ Rate limited (rare on dev tier!) - wait {self.rate_limit_delay}s")
                return self.rate_limit_delay, progress_made
            elif progress_made:
                print(f"✅ Progress made! Quick {self.success_delay}s break...")
                return self.success_delay, True
            elif result.returncode == 0:
                print(f"✅ Clean run completed!")
                return self.success_delay, False
            else:
                print(f"❌ Error (code: {result.returncode}) - retry in {self.retry_delay}s")
                return self.retry_delay, False
                
        except subprocess.TimeoutExpired:
            print("⏰ 20min timeout - likely working on complex task")
            return self.retry_delay, False
        except Exception as e:
            print(f"💥 Exception: {e}")
            return self.retry_delay, False
    
    def run_to_completion(self, max_runs=25):
        print("🚀 GENESIS FORGE - DEV TIER RUNNER")
        print("==================================")
        print("🏆 Goal: Complete all 10 major deliverables")
        print("⚡ Dev Tier: 250K tokens/min, 1K req/min")
        
        self.show_dashboard()
        
        total_tasks = len(self.completed_tasks)
        if sum(self.completed_tasks.values()) == total_tasks:
            print("\n🎉 PROJECT ALREADY COMPLETE!")
            return True
        
        start_time = datetime.now()
        
        for run in range(1, max_runs + 1):
            wait_time, progress_made = self.run_attempt(run)
            
            self.show_dashboard()
            
            completed = sum(self.completed_tasks.values())
            if completed == total_tasks:
                elapsed = datetime.now() - start_time
                print(f"\n🏆 GENESIS FORGE PROJECT COMPLETED!")
                print(f"⏱️  Total time: {elapsed}")
                print(f"📂 All deliverables in: deliverables/")
                print(f"🎯 Completed {total_tasks}/{total_tasks} tasks in {run} runs")
                return True
            
            if wait_time > 0 and run < max_runs:
                print(f"⏳ Waiting {wait_time}s... ({completed}/{total_tasks} done)")
                time.sleep(wait_time)
        
        # Final summary
        completed = sum(self.completed_tasks.values())
        print(f"\n📊 FINAL STATUS: {completed}/{total_tasks} completed")
        print(f"📂 Check deliverables/ folder for your work!")
        return completed == total_tasks

if __name__ == "__main__":
    print("🏗️  GENESIS FORGE - FINAL OPTIMIZED RUNNER")
    print("=" * 50)
    runner = OptimizedGenesisForgeCrew()
    success = runner.run_to_completion()
    
    if success:
        print("\n🎉 SUCCESS! Genesis Forge project complete!")
    else:
        print("\n⏸️  Paused - resume anytime by running again!")
