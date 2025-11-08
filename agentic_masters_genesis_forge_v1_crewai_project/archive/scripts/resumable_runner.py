import subprocess
import time
import os
import json
from datetime import datetime
import re

class ResumableGenesisForgeCrew:
    def __init__(self):
        self.progress_file = 'genesis_progress.json'
        self.deliverables_dir = 'deliverables'
        
        # Track completed tasks from logs
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
        """Extract task deliverable from output"""
        patterns = [
            r'Final Answer:\s*(.*?)(?=Agent:|Task Completed|$)',
            r'Assigned to:.*?Status: ✅ Completed.*?Final Answer:\s*(.*?)(?=┌|$)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, output_text, re.DOTALL | re.IGNORECASE)
            if matches:
                deliverable = matches[-1].strip()
                if deliverable and len(deliverable) > 100:
                    # Save deliverable
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
        """Analyze output to identify completed tasks"""
        completed_pattern = r'Task: (\w+).*?Status: ✅ Completed'
        completed_matches = re.findall(completed_pattern, output_text, re.DOTALL)
        
        for task_id in completed_matches:
            if task_id in self.completed_tasks:
                if not self.completed_tasks[task_id]:
                    print(f"✅ Task completed: {task_id}")
                    self.completed_tasks[task_id] = True
                    self.extract_deliverable(output_text, task_id)
    
    def get_next_task(self):
        """Get the next uncompleted task"""
        for task, completed in self.completed_tasks.items():
            if not completed:
                return task
        return None
    
    def run_with_resume(self, max_attempts=10):
        print("🚀 RESUMABLE GENESIS FORGE RUNNER")
        print("==================================")
        
        completed = sum(self.completed_tasks.values())
        total = len(self.completed_tasks)
        next_task = self.get_next_task()
        
        print(f"📊 Progress: {completed}/{total} tasks completed")
        if next_task:
            print(f"🎯 Next task: {next_task}")
        else:
            print("🎉 All tasks completed!")
            return True
        
        for attempt in range(1, max_attempts + 1):
            timestamp = datetime.now().strftime('%H%M%S')
            print(f"\n🔄 Attempt {attempt}/{max_attempts} - {datetime.now().strftime('%H:%M:%S')}")
            
            try:
                # Set environment
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                env['PYTHONUTF8'] = '1'
                
                # Run crew
                result = subprocess.run(
                    ['uv', 'run', 'run_crew'], 
                    capture_output=True, 
                    text=True, 
                    timeout=600,  # 10 min timeout
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
                if result.stdout:
                    self.analyze_output_for_completed_tasks(result.stdout)
                    self.save_progress()
                
                # Check if we made progress
                new_completed = sum(self.completed_tasks.values())
                if new_completed > completed:
                    print(f"🎉 Progress made! {new_completed}/{total} tasks completed")
                    completed = new_completed
                    next_task = self.get_next_task()
                    if next_task:
                        print(f"🎯 Next task: {next_task}")
                    else:
                        print("🏆 ALL TASKS COMPLETED!")
                        return True
                
                # Check for rate limit
                if result.returncode != 0 and "rate_limit" in str(result.stderr):
                    print("⏳ Rate limited - waiting 90s...")
                    time.sleep(90)
                elif result.returncode == 0:
                    print("✅ Run completed successfully!")
                    break
                else:
                    print(f"❌ Failed with code: {result.returncode}")
                    
            except subprocess.TimeoutExpired:
                print("⏰ Timeout after 10 minutes")
            except Exception as e:
                print(f"💥 Error: {e}")
            
            # Short wait between attempts
            if attempt < max_attempts:
                time.sleep(30)
        
        print(f"\n📈 Final Progress: {sum(self.completed_tasks.values())}/{total} tasks")
        print(f"📂 Check 'deliverables' folder for completed work!")

if __name__ == "__main__":
    runner = ResumableGenesisForgeCrew()
    runner.run_with_resume()
