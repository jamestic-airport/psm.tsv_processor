import os
import glob
import subprocess

def run_psm_processor(file_path, output_directory):
    if os.path.isfile(file_path):
        #print(f'run code on {file_path}')
        #print(f'Output: {output_directory}')
        subprocess.run(["python", "psm_processor.py", file_path, output_directory])
        

# Use glob to find all instances of psm.tsv recursively. This is a list of all psm.tsv paths
current_directory = os.getcwd()
psm_files = glob.glob(os.path.join(current_directory, "**", "psm.tsv"), recursive=True)

# Create the 'output' directory if it doesn't exist
output_directory = os.path.join(current_directory, 'output')
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Run psm_processor.py for each psm.tsv file found, passing the output_directory
for file_path in psm_files:
    run_psm_processor(file_path, output_directory)
# # Run psm_processor.py for each psm.tsv file found
# for file_path in psm_files:
#     run_psm_processor(file_path)