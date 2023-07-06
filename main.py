import os
import glob
import subprocess

def run_psm_processor(file_path, current_directory):
    directory_path = os.path.dirname(file_path) # Finds path to each directory containing psm.tsv
    #script_path = os.path.join(directory_path, "psm_processor.py")
    #print(script_path)
    print(file_path)
    if os.path.isfile(file_path):
        print(f'execute python script: python psm_processer.py {file_path}')
        subprocess.run(["python", "psm_processor.py", file_path])
        
# Get the current directory
current_directory = os.getcwd()

# Use glob to find all instances of psm.tsv recursively. This is a list of all psm.tsv paths
psm_files = glob.glob(os.path.join(current_directory, "**", "psm.tsv"), recursive=True)

# Run psm_processor.py for each psm.tsv file found
for file_path in psm_files:
    run_psm_processor(file_path, current_directory)