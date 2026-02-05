import subprocess
import os
import sys

def run_script(script_path, args=None):
    print(f"🚀 Executing: {os.path.basename(script_path)}...")
    cmd = ["python3", script_path]
    if args: cmd.extend(args)
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error in {os.path.basename(script_path)}:")
        print(res.stderr)
        return False
    print(res.stdout.strip())
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 orchestrator.py <path_to_new_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    scripts_dir = "zabio-analyst/scripts"
    
    # 1. Standardize entities
    if not run_script(os.path.join(scripts_dir, "correct_csv.py"), [csv_path]):
        sys.exit(1)
        
    # 2. Process data
    if not run_script(os.path.join(scripts_dir, "process_data.py"), [csv_path]):
        sys.exit(1)
        
    # 3. Generate visual output
    if not run_script(os.path.join(scripts_dir, "generate_dashboard.py")):
        sys.exit(1)
        
    print("\n✅ Weekly Update Complete. Dashboard updated at dashboard.html")

if __name__ == "__main__":
    main()
