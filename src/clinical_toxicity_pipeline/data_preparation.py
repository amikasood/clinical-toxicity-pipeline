import pandas as pd

def load_prepare_data(clinical_path, icu_path, hepato_path):
    '''
    Loads CSV files, merges them, and engineers features for modeling
    Parameters
    ----------
    clinical_path : Path to csv file containing the clinical data (subject_id,hadm_id,chembl_id,drug,itemid,time_of_exposure,baseline_val,peak_val,fold_change,Toxicity)
    icu_path : Path to scv file containing ICU drug names and times they were subscribed
    hepato_path : Path to scv file containing hepatotoxic drug names and their ChEMBL IDs
    Returns
    -------
    X, y
    '''
    print("Loading and merging CSV files")

    # Load data
    clinical_df = pd.read_csv(clinical_path)
    icu_df = pd.read_csv(icu_path)
    hepato_df = pd.read_csv(hepato_path)

    clinical_df['drug_lower'] = clinical_df['drug'].astype(str).str.lower()
    icu_df['drug_lower'] = icu_df['drug'].astype(str).str.lower()

    # Merge clinical data with ICU prescription counts
    df = pd.merge(clinical_df, icu_df[['drug_lower', 'Times prescribed']], on='drug_lower', how='left')
    df.rename(columns={'Times prescribed': 'icu_prescription_count'}, inplace=True)
    df['icu_prescription_count'] = df['icu_prescription_count'].fillna(0)

    # Create the hepatotoxic target flag using chembl_id
    #hepato_ids = set(hepato_df['chembl_id'].dropna().unique())
    #df['is_target_hepatotoxic'] = df['chembl_id'].apply(lambda x: 1 if x in hepato_ids else 0)

    # Define input feature X and target label y
    #X = df[['baseline_val', 'peak_val', 'fold_change', 'icu_prescription_count', 'is_target_hepatotoxic']]
    X = df[['baseline_val', 'icu_prescription_count', 'is_target_hepatotoxic']]
    y = df['Toxicity']

    return X, y