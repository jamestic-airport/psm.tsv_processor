import os
import glob
import subprocess

def make_output_directory():
    output_directory = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return output_directory

# Use glob to find all instances of psm.tsv recursively. This is a list of all psm.tsv paths
def find_all_psm_files():
    files = glob.glob(os.path.join(os.getcwd(), "**", "psm.tsv"), recursive=True)
    return files

def run_psm_processor(file_path, output_directory):
    if os.path.isfile(file_path):
        print(f'Analysing {file_path}...')
        subprocess.run(["python", "psm_processor.py", file_path, output_directory])
        

########################
##### MAIN SCRIPT ######
########################

output_directory = make_output_directory()
psm_files = find_all_psm_files()

# Run psm_processor.py for each psm.tsv file found, passing the output_directory
for file_path in psm_files:
    run_psm_processor(file_path, output_directory)
