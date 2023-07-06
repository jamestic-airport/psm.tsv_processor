import os
import glob
import subprocess

def run_psm_processor(file_path):
    if os.path.isfile(file_path):
        #print(f'execute python script: python psm_processor.py {file_path}')
        subprocess.run(["python", "psm_processor.py", file_path])
        

# Use glob to find all instances of psm.tsv recursively. This is a list of all psm.tsv paths
current_directory = os.getcwd()
psm_files = glob.glob(os.path.join(current_directory, "**", "psm.tsv"), recursive=True)

# Run psm_processor.py for each psm.tsv file found
for file_path in psm_files:
    run_psm_processor(file_path)