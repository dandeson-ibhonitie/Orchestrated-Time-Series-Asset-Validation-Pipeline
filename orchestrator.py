import subprocess
import time
import sys

def execute_node(script_name):
    """
    Executes a single pipeline script as an isolated process.
    """
    print(f"\n==================== RUNNING: {script_name} ====================")
    start_time = time.time()
    

    process = subprocess.run([sys.executable, script_name], text=True)
    
    elapsed_time = time.time() - start_time
    
    # A returncode of 0 means the script finished with zero errors
    if process.returncode != 0:
        print(f"\n PIPELINE CRITICAL HALT: '{script_name}' encountered an error or crashed.")
        return False, elapsed_time
        
    print(f" SUCCESS: '{script_name}' completed cleanly. Run time: {elapsed_time:.2f}s")
    return True, elapsed_time

def main():
    pipeline_start = time.time()
    
    # dictates the absolute execution order of the pipeline assembly line
    pipeline_manifest = ["1_extract.py", "2_transform.py", "3_load.py"]
    performance_metrics = {}
    
    print("Initializing Master Automation Control Layer...")
    
    # Loop through the pipeline chain-reaction sequence
    for script in pipeline_manifest:
        success, duration = execute_node(script)
        performance_metrics[script] = duration
        
        # If any script fails, stop the entire conveyor belt immediately to protect data integrity
        if not success:
            print("\nPipeline execution aborted due to downstream dependency failure.")
            sys.exit(1)
            
    total_pipeline_time = time.time() - pipeline_start
    
    # Generate the final system tracking report
    print("\n" + "="*65)
    print(" FINAL UNIFIED SYSTEM EXECUTION TIMELINE PERFORMANCE REPORT 🏁")
    print("="*65)
    for script, duration in performance_metrics.items():
        print(f" * Node Process: {script:<15} | Operational Window: {duration:.4f} seconds")
    print("-"*65)
    print(f"TOTAL AUTOMATION RUN TIME FOOTPRINT: {total_pipeline_time:.4f} seconds")
    print("="*65)

if __name__ == "__main__":
    main()
