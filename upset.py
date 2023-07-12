# Given an excel file
# Iterates through the sheets
# For each sheet, it generates an upset plot with the relevant sheet name

import pandas as pd
import pprint
from upsetplot import from_contents, UpSet
from matplotlib import pyplot

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

def generate_upset_plots(ptm_type, ptm_dict):
    print(f'Generating upset plot for {ptm_type}...')
    upset = from_contents(ptm_dict)
    ax_dict = UpSet(upset, subset_size='count').plot()
    #pyplot.show()   
    pyplot.savefig(f"{ptm_type}.pdf")  
    

excel_file = get_input_file()
for sheet in excel_file.sheet_names:
    ptm_dict = get_dict(sheet)
    generate_upset_plots(sheet, ptm_dict)
    
print('Upset Plot Generation Complete!')

