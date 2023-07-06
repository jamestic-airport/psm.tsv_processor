import pandas as pd

excel_file = pd.ExcelFile('psm_output.xlsx')
counts = {}

for sheet_name in excel_file.sheet_names:

    df = excel_file.parse(sheet_name)

    # mod_site_counts is a df containing the localisation site and its frequency
    mod_site_counts = df['Full Localisation Sites'].value_counts().reset_index()     
    mod_site_counts.columns = ['Value', 'Count']
    # counts is a dict of dfs. The keys are the modification types.
    counts[sheet_name] = mod_site_counts     

with pd.ExcelWriter('Localization Summary.xlsx') as writer:

    for sheet_name, mod_site_counts in counts.items():
        mod_site_counts.to_excel(writer, sheet_name=sheet_name, index=False)
