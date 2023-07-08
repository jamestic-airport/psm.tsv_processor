import pandas as pd
import os
import pprint

def get_files():
    excel_files = []
    directory = os.path.join(os.getcwd(), 'output')
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):  # Check if it's an Excel file
            #file_path = os.path.join(directory, filename)
            excel_files.append(filename)
    return excel_files


def get_ptm_counts(file_name):

    directory = os.path.join(os.getcwd(), 'output')
    file_path = os.path.join(directory, file_name)

    df_all = pd.DataFrame()
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        # mod_site_counts is a df containing the localisation site and its frequency
        mod_site_counts = df['Full Localisation Sites'].value_counts().reset_index()     
        mod_site_counts.columns = ['Value', 'Count']
        mod_site_counts.insert(0, 'PTM', sheet_name)
        df_all = pd.concat([df_all, mod_site_counts], ignore_index=True)
    return df_all

def add_database_names(df, file_name):
    print(file_name)
    df.insert(0, 'Dataset', file_name)
    return df

def create_file(df):
    print(df)
    df.to_excel('PTM Mod Site Summary.xlsx', index=False)  # Specify the file name and remove index column


# Iterate over each file in the directory

all_counts = pd.DataFrame()

files = get_files()
for file in files:
    counts = get_ptm_counts(file)
    counts = add_database_names(counts, file)
    all_counts = pd.concat([all_counts, counts], ignore_index=True)


create_file(all_counts)





