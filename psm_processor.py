import pandas as pd

# This program reads in a psm.tsv file from MSFragger. Its main purpose is to only select rows
# which are appropriate human ribosomal proteins. 
#  
# psm_rp_only is simply a .tsv file only containins ribosomal proteins

#######################
# FILTERING FUNCTIONS #
#######################

# Given a df containing standard MSFragger psm.tsv output, it isolates ribosomal proteins. This list of RPs can be modified in the 
# accompanying excel file. Entries with no Observed Modifications are also removed. Any empty MSFragger Localization cells 
# are replaced with 'NONE'
def filter_RPs(chunk, ENTRY_NAMES):
    df = chunk[chunk['Entry Name'].isin(ENTRY_NAMES)]
    filtered_df = df.dropna(subset=['Observed Modifications'])
    filtered_df.loc[filtered_df['MSFragger Localization'].isna(), 'MSFragger Localization'] = "NONE"
    return filtered_df

# Certain PTMs are only expected to be found on specific amino acid residues. 
# This function takes in a df of one PTM type, and a list of amino acids.
# It searches for entries with a localisation site that matches one of the provided amino_acids. 
def filter_amino_acids(df, amino_acids):
    amino_acids = '[' + ''.join(amino_acids) + ']'
    aa_mask = df['MSFragger Localization'].str.contains(amino_acids, case=True, regex=True)
    df = df[aa_mask]
    return df

# In MSFragger closed searches, methylation has the following entries:
#   Methyl, DiMethyl/Ethyl, TriMethylation    
# In MSFragger open searches, methylation has the following entries:
#   Methylation, di-Methylation, tri-Methylation
# This functions finds all relevant methylation modifications. 
# Entries with an expected localisation site are selected. In methylation, this is Lysine (K) and Arginine (R).
# Potential N-terminal modifications are also selected
def filter_methyl(df):
    
    mask = df['Observed Modifications'].str.contains('1: Methyl|1: DiMethyl|1: TriMethyl')
    methyl_mods = df[mask]

    mods = filter_amino_acids(methyl_mods, ['r', 'k']) # 
    nterm_mods = methyl_mods[methyl_mods['Protein Start'] <= 5]

    methyl_df = pd.concat([mods, nterm_mods], ignore_index = True)

    return methyl_df

# In MSFragger closed searches, phosphorylation has the following entries:
#   Phospho   
# In MSFragger open searches, phosphorylation has the following entries:
#   Phosphorylation
# This functions finds all relevant phosphorylation modifications. 
# Entries with an expected localisation site are selected. In phosphorylation, this is Serine (S), Threonine (T) and Tyrosine (Y).
# Potential N-terminal modifications are also selected
def filter_phospho(df):
    
    mask = df['Observed Modifications'].str.contains('1: Phospho')
    phospho_mods = df[mask]

    mods = filter_amino_acids(phospho_mods, ['s', 't', 'y'])
    nterm_mods = phospho_mods[phospho_mods['Protein Start'] <= 5]

    phospho_df = pd.concat([mods, nterm_mods], ignore_index = True)

    return phospho_df

# In MSFragger closed searches, acetylation has the following entries:
#   Acetyl   
# In MSFragger open searches, acetylation has the following entries:
#   Acetylation
# This functions finds all relevant acetylation modifications. 
# Entries with an expected localisation site are selected. In acetylation, this is ????.
# Potential N-terminal modifications are also selected
def filter_acetyl(df):
    
    mask = df['Observed Modifications'].str.contains('1: Acetyl')
    acetyl_mods = df[mask]
    
    mods = filter_amino_acids(acetyl_mods, ['r', 'k', 's', 't', 'y'])
    nterm_mods = acetyl_mods[acetyl_mods['Protein Start'] <= 5]

    acetyl_df = pd.concat([mods, nterm_mods], ignore_index = True)

    return acetyl_df


##########################
# lOCALISATION FUNCTIONS #
##########################

# Lowercase letters indicate localisation sites through the MSFragger Localisation algorithm.
# Finds all lowercase letters from a sequence of amino acids and returns the amino acid
# and its position in the sequence. This position can be 'N-terminal'.
def find_localisation_position(sequence, start, ptm):
    start = int(start)
    localised_sites = []
    for index, char in enumerate(sequence):
        if char.islower():
            localised_sites.append((index + start, char))
    localised_sites = clean_localised_sites(localised_sites, ptm)
    return localised_sites

# Starts with a list of tuples [(2, 'a'), (3, 's'), (4, 'v')] and converts 
# it to a clean list that looks like A2, S3, V4.
# If the number is 2, this modification is classified as an N terminal modification
# Only relevant amino acids are selected based on the given ptm type.
def clean_localised_sites(localised_sites, ptm):
    clean_sites = []    
    for num, char in localised_sites:
        if num == 2:
            return 'N-terminal'
        if ptm == 'methyl':
            if char in ['r', 'k']:   
                clean_sites.append(char.upper() + str(num))
        if ptm == 'phospho':
            if char in ['s', 't', 'y']:   
                clean_sites.append(char.upper() + str(num))
        if ptm == 'acetyl':
            if char in ['r', 'k', 's', 't', 'y']:   
                clean_sites.append(char.upper() + str(num))
    delimiter = ', '
    clean_sites = delimiter.join(clean_sites)   
    if len(clean_sites) == 0:
        return 'NONE'
    return clean_sites

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

        # Filter based on observed modification and appropriate amino acid being modified. 
        # Search for normal and N-terminal modifications
        methyl_chunk = filter_methyl(RP_chunk)
        phospho_chunk = filter_phospho(RP_chunk)
        acetyl_chunk = filter_acetyl(RP_chunk)

        # Apply localisation to all chunks and append a column of all potential modification sites
        # Filter out any 'bad' N-terminal modifications
        methyl_chunk['Localised Sites'] = methyl_chunk.apply(lambda row: find_localisation_position(row['MSFragger Localization'], row['Protein Start'], 'methyl'), axis=1)
        phospho_chunk['Localised Sites'] = phospho_chunk.apply(lambda row: find_localisation_position(row['MSFragger Localization'], row['Protein Start'], 'phospho'), axis=1)
        acetyl_chunk['Localised Sites'] = acetyl_chunk.apply(lambda row: find_localisation_position(row['MSFragger Localization'], row['Protein Start'], 'acetyl'), axis=1)

        #Write all chunks to separate sheets in excel
        methyl_chunk.to_excel(writer, sheet_name='Methylation', index=False)
        phospho_chunk.to_excel(writer, sheet_name='Phosphorylation', index=False)
        acetyl_chunk.to_excel(writer, sheet_name='Acetylation', index=False)

        RP_chunk.to_csv('psm_rp_only.tsv', sep='\t', index=False)


# print(find_localisation_position('KQSGYGGQTkPIFR'))
# print(find_localisation_position('KDLLHPSPEEE'))
# print(find_localisation_position('KDLLHpsPEEE'))
