import pandas as pd
import os
import pprint

def get_counts(file_path):

    df_all = pd.DataFrame()
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        # mod_site_counts is a df containing the localisation site and its frequency
        mod_site_counts = df['Full Localisation Sites'].value_counts().reset_index()     
        mod_site_counts.columns = ['Value', 'Count']
        mod_site_counts.insert(0, 'PTM', sheet_name)
        mod_site_counts.insert(0, 'Dataset', file_path)
        df_all = pd.concat([df_all, mod_site_counts], ignore_index=True)
    return df_all


def get_excel_files():

    excel_files = []
    directory = os.path.join(os.getcwd(), 'output')
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):  # Check if it's an Excel file
            file_path = os.path.join(directory, filename)
            excel_files.append(file_path)
    return excel_files


def create_file(df):
    print(df)
    df.to_excel('Localization Summary Test 1.xlsx', index=False)  # Specify the file name and remove index column


# Iterate over each file in the directory

all_counts = pd.DataFrame()
excel_files = get_excel_files()
for file in excel_files:
    counts = get_counts(file)
    all_counts = pd.concat([all_counts, counts], ignore_index=True)

create_file(all_counts)



