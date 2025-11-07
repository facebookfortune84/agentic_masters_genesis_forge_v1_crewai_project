import subprocess
import time
import os
import json
from datetime import datetime
import re

class EnhancedResumableRunner:
    def __init__(self):
        self.progress_file = 'genesis_progress.json'
        self.deliverables_dir = 'deliverables'
        
        # Track all tasks
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
        
        # Smart pacing - longer delays
        self.base_delay = 180  # 3 minutes base
        self.rate_limit_delay = 300  # 5 minutes after rate limit
        
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
            'last_run': datetime.now().isoformat()
        }
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def extract_deliverable(self, output_text, task_name):
        patterns = [
            r'Final Answer:\s*(.*?)(?=Agent:|Task Completed|┌|$)',
            r'Assigned to:.*?Status: ✅ Completed.*?Final Answer:\s*(.*?)(?=┌|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, output_text, re.DOTALL | re.IGNORECASE)
            if matches:
                deliverable = matches[-1].strip()
                if deliverable and len(deliverable) > 100:
                    timestamp = datetime.now().strftime('%H%M%S')
                    filename = f"{self.deliverables_dir}/{task_name}_{timestamp}.md"
                    with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(f"# {task_name.replace('_', ' ').title()}\n\n")
                        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write(deliverable)
                    print(f"💾 Saved deliverable: {filename}")
                    return True
        return False
    
    def analyze_output_for_completed_tasks(self, output_text):
        completed_pattern = r'Task: (\w+).*?Status: ✅ Completed'
        completed_matches = re.findall(completed_pattern, output_text, re.DOTALL)
        
        for task_id in completed_matches:
            if task_id in self.completed_tasks:
                if not self.completed_tasks[task_id]:
                    print(f"✅ Task completed: {task_id}")
                    self.completed_tasks[task_id] = True
                    self.extract_deliverable(output_text, task_id)
    
    def get_next_task(self):
        for task, completed in self.completed_tasks.items():
            if not completed:
                return task
        return None
    
    def show_status(self):
        completed = sum(self.completed_tasks.values())
        total = len(self.completed_tasks)
        
        print(f"\n📊 GENESIS FORGE PROGRESS: {completed}/{total} tasks")
        print("=" * 50)
        
        for task, done in self.completed_tasks.items():
            status = "✅" if done else "⏳"
            print(f"{status} {task.replace('_', ' ').title()}")
        
        if completed < total:
            next_task = self.get_next_task()
            print(f"\n🎯 Next: {next_task.replace('_', ' ').title()}")
        else:
            print("\n🏆 ALL TASKS COMPLETED!")
    
    def run_single_attempt(self, attempt):
        timestamp = datetime.now().strftime('%H%M%S')
        print(f"\n🚀 Attempt {attempt} - {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            result = subprocess.run(
                ['uv', 'run', 'run_crew'], 
                capture_output=True, 
                text=True, 
                timeout=900,  # 15 min timeout
                env=env,
                encoding='utf-8',
                errors='ignore'
            )
            
            # Save output
            output_file = f"outputs/attempt_{attempt}_{timestamp}.log"
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(f"Return Code: {result.returncode}\n")
                f.write(f"STDOUT:\n{result.stdout}\n")
                f.write(f"STDERR:\n{result.stderr}\n")
            
            print(f"📁 Saved: {output_file}")
            
            # Analyze progress
            initial_completed = sum(self.completed_tasks.values())
            if result.stdout:
                self.analyze_output_for_completed_tasks(result.stdout)
                self.save_progress()
            
            new_completed = sum(self.completed_tasks.values())
            progress_made = new_completed > initial_completed
            
            # Determine wait time
            if "rate_limit" in str(result.stderr):
                print(f"⏳ Rate limited - waiting {self.rate_limit_delay}s...")
                return self.rate_limit_delay, progress_made
            elif progress_made:
                print(f"✅ Progress made! Waiting {self.base_delay}s...")
                return self.base_delay, progress_made
            elif result.returncode == 0:
                print("✅ Run completed successfully!")
                return 0, progress_made
            else:
                print(f"❌ Failed with code: {result.returncode}")
                return self.base_delay, progress_made
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout after 15 minutes")
            return self.base_delay, False
        except Exception as e:
            print(f"💥 Error: {e}")
            return self.base_delay, False
    
    def run_continuous(self, max_attempts=20):
        print("🚀 ENHANCED GENESIS FORGE RUNNER")
        print("================================")
        
        self.show_status()
        
        if sum(self.completed_tasks.values()) == len(self.completed_tasks):
            print("🎉 All tasks already completed!")
            return True
        
        for attempt in range(1, max_attempts + 1):
            wait_time, progress_made = self.run_single_attempt(attempt)
            
            self.show_status()
            
            if sum(self.completed_tasks.values()) == len(self.completed_tasks):
                print("🏆 ALL TASKS COMPLETED!")
                return True
            
            if wait_time > 0 and attempt < max_attempts:
                mins = wait_time // 60
                secs = wait_time % 60
                print(f"⏳ Waiting {mins}m {secs}s before next attempt...")
                time.sleep(wait_time)
        
        completed = sum(self.completed_tasks.values())
        total = len(self.completed_tasks)
        print(f"\n📈 Final: {completed}/{total} tasks completed")
        print(f"📂 Check 'deliverables/' folder for your work!")
        
        return completed == total

if __name__ == "__main__":
    runner = EnhancedResumableRunner()
    runner.run_continuous()
