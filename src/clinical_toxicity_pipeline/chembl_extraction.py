import requests
import pandas as pd
import time
import os
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # from src/clinical_toxicity_pipeline/
csv_path = PROJECT_ROOT / "data" / "raw" / "top_50_icu_drugs.csv"

# Read drug target list from a csv file data/raw/top_50_icu_drugs.csv and an empty Dictionary
#drug_targets = ['aspirin', 'ibuprofen', 'acetaminophen', 'lisinopril', 'metformin']
drug_targets = pd.read_csv(csv_path)['drug'].dropna().tolist()
drug_smiles_dict = {}

print(f"Successfully read {len(drug_targets)} drug targets from the csv file")

# Loop through each drug target
# add print statements to show the progress
for target in drug_targets:
    # Define the API endpoint URL
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search.json?q={target}"
    # Send a GET request to the API endpoint
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Explicitly check if the API returned an empty list of molecules
        if not data.get('molecules'):
            print(f"Warning: No ChEMBL record found for '{target}'")
            drug_smiles_dict[target] = "Not Found"
            
        else:
            # Grab the structure dictionary safely
            structures = data['molecules'][0].get('molecule_structures')
            
            # Check if the structure is None (which caused your crash)
            if structures is None:
                print(f"Warning: No structural data available for '{target}'")
                drug_smiles_dict[target] = "No Structure"
            else:
                # Safely extract the SMILES
                smiles = structures.get('canonical_smiles', 'No Canonical SMILES')
                drug_smiles_dict[target] = smiles
                print(f"Successfully extracted: {target.capitalize()}")
                
    else:
        print(f"API Ping Failed for '{target}'. Status Code: {response.status_code}")

# Convert Dictionary to DataFrame
drug_smiles_df = pd.DataFrame(drug_smiles_dict.items(), columns=['Drug Target', 'SMILES'])