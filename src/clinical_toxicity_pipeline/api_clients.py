from __future__ import annotations
import pandas as pd
import requests
from typing import Any, cast

from chembl_webresource_client.new_client import new_client

def fetch_icu_smiles(input_csv_path, output_csv_path):
    '''
    Fetches SMILES strings for a list of ICU medications.
    Paratemers
    ----------
    input_csv_path : Path to csv file containing list of ICU medications
    Returns
    -------
    output_csv_path : Path to csv files with Drug name and corresponding SMILES string
    '''
    print("Fetching SMILES strings for a list of ICU medications")
    drug_targets = pd.read_csv(input_csv_path)['drug'].dropna().to_list()
    drug_smiles_dict = {}

    #Loop through each drug target and extract SMILES
    for target in drug_targets:
        url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search.json?q={target}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if not data.get('molecules'):
                drug_smiles_dict[target] = "Not Found"
            else:
                structures = data['molecules'][0].get('molecule_structures')
                if structures is None:
                    drug_smiles_dict[target] = "No Structure"
                else:
                    drug_smiles_dict[target] = structures.get('canonical_smiles', 'No Canonical SMILES')
        else:
            print(f"API ping failed for {target}")
    
    df = pd.DataFrame(list(drug_smiles_dict.items()), columns=['Drug', 'SMILES'])
    df.to_csv(output_csv_path, index=False)
    print(f"SMILES dtata saved to {output_csv_path}")

def fetch_hepatotoxic_drugs(output_csv_path):
    '''
    Fetches 50 hepatotoxic drugs from ChEMBL.
    Returns
    -------
    output_csv_path : path to csv file containing top 50 hepatotoxic drugs with their ChEMBL ID and names.
    '''
    print("Fetching Hepatotoxic warnings from ChEMBL")
    drug_warning = new_client.drug_warning
    res = drug_warning.filter(warning_class__icontains='hepatotoxicity')
    res_df = pd.DataFrame(res)

    chembl_ids = list(res_df['parent_molecule_chembl_id'])

    molecule = new_client.molecule
    res_mols = molecule.filter(molecule_chembl_id__in=chembl_ids).only(['molecule_chembl_id', 'pref_name'])

    drugs = []
    for d in res_mols:
        if d['pref_name'] is not None:
            drugs.append({
                'chembl_id': d['molecule_chembl_id'],
                'pref_name': d['pref_name'].lower()
            })
        if len(drugs) >= 50:
            break
    
    df = pd.DataFrame(drugs)
    df.to_csv(output_csv_path, index=False)
    print(f"Saved {len(df)} hepatotoxic records to {output_csv_path}")