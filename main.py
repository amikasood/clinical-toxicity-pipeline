"""CLI entry point for the clinical toxicity pipeline."""

from __future__ import annotations

import argparse
import os
from sklearn.model_selection import train_test_split

#from src.clinical_toxicity_pipeline.api_clients import fetch_icu_smiles, fetch_hepatotoxic_drugs
from src.clinical_toxicity_pipeline.data_preparation import load_prepare_data
from src.clinical_toxicity_pipeline.xgboost import run_xgboost
from src.clinical_toxicity_pipeline.dl_model import run_baseline


def run() -> None:
    icu_path = 'data/raw/top_50_icu_drugs.csv'
    clinical_path = 'data/raw/clinical_data_updated.csv'
    hepato_path = 'data/raw/target_hepatotoxic_drugs.csv'
    smiles = 'data/raw/icu_drug_smiles.csv'

    #Data collection
    #Fetch SMILES string for each target drug and 50 hapetotoxic  drugs
    #print("----- Running Data Collection -----")
    #fetch_icu_smiles(icu_path, smiles)
    #fetch_hepatotoxic_drugs(hepato_path)

    X, y = load_prepare_data(clinical_path, icu_path, hepato_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    #print(X[X['is_target_hepatotoxic']==1])
    run_xgboost(X_train, y_train, X_test, y_test)
    run_baseline(X_train, y_train,X_test,y_test)


if __name__ == "__main__":
    run()
