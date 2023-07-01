import pandas as pd

# This program reads in a psm.tsv file from MSFragger. Its main purpose is to only select rows
# which are appropriate human ribosomal proteins. 
#  
# psm_rp_only is simply a .tsv file only containins ribosomal proteins

def filter_RPs(chunk, ENTRY_NAMES):
    filtered_df = chunk[chunk['Entry Name'].isin(ENTRY_NAMES)]
    filtered_df.dropna(subset=['Observed Modifications'], inplace=True)

    return filtered_df

def filter_amino_acids(df, amino_acids):
    
    amino_acids = '[' + ''.join(amino_acids) + ']'
    aa_mask = df['MSFragger Localization'].str.contains(amino_acids, case=True, regex=True)
    df = df[aa_mask]
    return df

def filter_methyl(df):
    
    mask = df['Observed Modifications'].str.contains('1: Methyl|1: DiMethyl|1: TriMethyl')
    methyl_df = df[mask]
    methyl_df = filter_amino_acids(methyl_df, ['r', 'k']) # Lysine (K) and Arginine (R) are most commonly methylated

    return methyl_df

def filter_phospho(df):
    
    mask = df['Observed Modifications'].str.contains('1: Phospho')
    phospho_df = df[mask]
    phospho_df = filter_amino_acids(phospho_df, ['s', 't'])

    return phospho_df

def filter_acetyl(df):
    
    mask = df['Observed Modifications'].str.contains('1: Acetyl')
    acetyl_df = df[mask]
    #print(acetyl_df)

    return acetyl_df


####################
### psm_rp_only ####
####################
# This file only includes the ribosomal proteins that are found in psm.tsv 

# Create a set of Entry Names to filter names in psm.tsv
df = pd.read_excel('Human_Ribosome_List.xlsx')
ENTRY_NAMES = set(df['Entry Name'])
chunk_size = 1000000 # 1 million rows per chunk

with pd.ExcelWriter('psm_output.xlsx') as writer:

    for chunk in pd.read_csv('psm_test.tsv', delimiter='\t', chunksize=chunk_size):

        RP_chunk = filter_RPs(chunk, ENTRY_NAMES)

        methyl_chunk = filter_methyl(RP_chunk)
        phospho_chunk = filter_phospho(RP_chunk)
        acetyl_chunk = filter_acetyl(RP_chunk)

        methyl_chunk.to_excel(writer, sheet_name='Methylation', index=False)
        phospho_chunk.to_excel(writer, sheet_name='Phosphorylation', index=False)
        acetyl_chunk.to_excel(writer, sheet_name='Acetylation', index=False)

        RP_chunk.to_csv('psm_rp_only.tsv', sep='\t', index=False)



    