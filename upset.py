# Given an excel file
# Iterates through the sheets
# For each sheet, it generates an upset plot with the relevant sheet name

import pandas as pd
import pprint
from upsetplot import from_contents, UpSet
from matplotlib import pyplot
import os
import shutil

def get_input_file():
    excel_file = pd.ExcelFile('summary output/Summary by PTM.xlsx')
    return excel_file

# Create a dict based on df. The keys will be the unique 
# entries in the 'Dataset' column. 
def get_dict(sheet):
    ptm_dict = {}
    df = excel_file.parse(sheet)
    for index, row in df.iterrows(): # Returns a tuple if just row
        key = row['Dataset']
        mod_site = row['Value']
        if key in ptm_dict:
            ptm_dict[key].append(mod_site)
        else:
            ptm_dict[key] = [mod_site]
    return ptm_dict

def create_output_folder():
    path = os.path.join(os.getcwd(), 'upset plot output')
    if os.path.exists(path):
        # If the folder already exists, remove it
        print("Overwriting pre-existing upset plot output folder...") 
        shutil.rmtree(path)

    os.makedirs(path)

def generate_upset_plots(ptm_type, ptm_dict):
    print(f'Generating upset plot for {ptm_type}...')
    upset = from_contents(ptm_dict)
    ax_dict = UpSet(upset, subset_size='count').plot()
    #pyplot.show()   
    pyplot.savefig(f"upset plot output/{ptm_type}.pdf")  
    

excel_file = get_input_file()
create_output_folder()
for sheet in excel_file.sheet_names:
    ptm_dict = get_dict(sheet)
    generate_upset_plots(sheet, ptm_dict)
    
print('Upset Plot Generation Complete!')

