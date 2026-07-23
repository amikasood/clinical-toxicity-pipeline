import pandas as pd

# Python script to extract 50 hepatotoxic drugs from ChEMBL and save chembl id and drug name to a csv file
from chembl_webresource_client.new_client import new_client
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # from src/clinical_toxicity_pipeline/
csv_path = PROJECT_ROOT / "data" / "raw" / "target_heptotoxic_drugs.csv"

# Find drugs with hepatotoxicity warning
drug_warning = new_client.drug_warning
res = drug_warning.filter(warning_class__icontains='hepatotoxicity')
res = pd.DataFrame(res)

# Extract parent_chembl_ids from these drugs
chembl_ids = list(res['parent_molecule_chembl_id'])

# Use Chembl IDs to get the drug name
print(f"Found {len(chembl_ids)} hepatotoxic IDs. Fetching names...")
molecule = new_client.molecule
res = molecule.filter(molecule_chembl_id__in=chembl_ids).only(['molecule_chembl_id','pref_name'])

drugs = []
for d in res:
    if d['pref_name'] is not None:
        drugs.append({
            'chembl_id': d['molecule_chembl_id'],
            'pref_name': d['pref_name'].lower()
        })
    if len(drugs) >= 50:
        break

# Convert drugs to a dataframe and save as csv
df = pd.DataFrame(drugs)
df.to_csv(csv_path, index=False)

print(drugs)




