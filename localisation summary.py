import pandas as pd
import os
import pprint

def get_psm_processor_output_files():
    excel_files = []
    directory = os.path.join(os.getcwd(), 'output')
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):  # Check if it's an Excel file
            excel_files.append(filename)
    return excel_files


def get_ptm_counts(file_name):

    file_path = os.path.join(os.getcwd(), 'output', file_name)

    df_all = pd.DataFrame()
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        mod_site_counts = df['Full Localisation Sites'].value_counts().reset_index()     
        mod_site_counts.columns = ['Value', 'Count']
        mod_site_counts.insert(0, 'PTM', sheet_name)
        df_all = pd.concat([df_all, mod_site_counts], ignore_index=True)
    return df_all


def add_database_names(df, file_name):
    df.insert(0, 'Dataset', file_name[:-5]) # Removes .xlsx from the end
    return df

def create_output_folder():
    path = os.path.join(os.getcwd(), 'summary output')
    if os.path.exists(path):
        # If the folder already exists, remove it
        print("Overwriting pre-existing summary output folder...")
        os.rmdir(path)

    os.makedirs(path)

def create_output_files(df):

    # Overall summary
    df.to_excel('summary output/summary.xlsx', index=False)  # Specify the file name and remove index column

    # Summary separated by PTM type
    with pd.ExcelWriter('summary output/summary by PTM.xlsx') as excel_file:

        for ptm, group in df.groupby('PTM'):
            group.to_excel(excel_file, sheet_name=ptm, index=False)


##################
##### MAIN  ######
##################

all_counts = pd.DataFrame()

for file_name in get_psm_processor_output_files():
    counts = get_ptm_counts(file_name)
    add_database_names(counts, file_name)
    all_counts = pd.concat([all_counts, counts], ignore_index=True)

create_output_folder()
create_output_files(all_counts)





