# Translational Risk Platform: Unified Molecular and Clinical AI

## The Problem
The pharmaceutical industry faces about a 90% failure rate for drug candidates entering clinical trials [1][2]. The direct cost of conducting Phase II studies can range from $7 million to nearly $20 million per trial, with overall failed drug development costing billions [3]. A major reason is that traditionally risk assessment is partitioned between cheminformaticians who evaluate the 2D/3D molecular structure for toxicity, and clinical biostatisticians who evaluate the trial protocol for patient cohort risks. Both of these evaluations tend to be carried out in silos.     

**The Solution:** This project bridges the translational gap. This AI pipeline takes a proposed drug's SMILES string and its Phase II/III clinical trial protocol, and generates a unified risk score that predicts the likelihood of trial failure due to adverse events (specifically hepatotoxicity).

## How it works
The project is divided into two phases:
1. **The Molecular Deep Learning Engine (Chem2Clinic):** A Pytorch Geometric Graph Neural Network (GNN) that ingests 2D molecular graphs to predict structural toxicity. *(In Development)*
2. **Clinical AI Agent (TrialGraph):** An LLM-driven agent that parses unstructured trial protocols and synthesize a final failure risk report. *(Planned)*    

## Current Progress: The Baselines
Before building the deep learning graph architecture, a baseline was established using standard tabular clinical data to prove that hospital demographics and generic flags alone are not sufficient to predict chemical toxicity.

### 1. Data Engineering (SQL and BigQuery)
Using the MIMIC-IV clinical database, a standardized clinical dataset was created with SQL.
* Common Table Expressions (CTEs) were used to isolate first-exposure administration events across the top 200 most frequently prescribed hospital medications.
* Performed a `LEFT JOIN` against known hepatotoxic ChEMBL IDs to create a balanced dataset containing both safe and toxic medications.
* Mapped pre-exposure baseline lab values (ALT/AST) and calculated `Toxicity` targets based on a 3.0+ fold change.

### 2. Modeling & Results
Two baseline models were built to predict toxicity using only pre-exposure clinical features (`baseline_val`, `icu_prescription_count`, `is_target_hepatotoxic`). To prevent data leakage, post-exposure lab metrics (`peak_val` and `fold_change`) were excluded:
* **XGBoost Classifier:** Handled severe class imbalance using `scale_pos_weight=30`. Peaked at an F1-Score of 0.06 and a PR-AUC of 0.04.
* **PyTorch Multi-Layer Perceptron (MLP):** A standard feed-forward neural network on the tabular features. Peaked at an F1-Score of 0.00 and a PR-AUC of 0.02. 

**Conclusion:** The low baseline scores prove that tabular hospital data and generic warning flags lack the necessary chemical context to predict complex adverse events. Therefore, it is necessary to use a PyTorch GNN to analyze the 2D molecular structures (SMILES) of the medications.

## Repository Structure
This project follows an industry-standard `src` layout:

```text
clinical-toxicity-pipeline/
├── data/
│   └── raw/                            # (Ignored in Git) Raw CSV extracts from MIMIC-IV and ChEMBL
├── sql/
│   └── create_toxicity_labels.sql      # BigQuery SQL for dynamic cohort generation
├── main.py                             # CLI Orchestrator for the pipeline
└── src/
    └── clinical_toxicity_pipeline/
        ├── api_clients.py              # Scripts to pull SMILES and target data via ChEMBL API
        ├── data_preparation.py         # Pandas logic for merging and cleaning clinical datasets
        ├── xgboost.py                  # Classical ML baseline and evaluation metrics
        └── dl_model.py                 # PyTorch deep learning architecture (MLP & GNN WIP)
```

## Execution
Pipeline actions are controlled via the primary command-line interface:

```
Bash

# Extract molecular SMILES descriptors via ChEMBL API
python main.py --action fetch_data

# Execute XGBoost baseline evaluation
python main.py --action train_xgb

# Execute PyTorch tabular MLP baseline evaluation
python main.py --action train_pytorch
```

References
1. DrugPatentWatch. "Beyond the Balance Sheet: Using Patent Data to De-Risk Pharma Investments." DrugPatentWatch, 12 Feb. 2026, https://www.drugpatentwatch.com/blog/beyond-the-balance-sheet-using-patent-data-to-de-risk-pharma-investments/.

2. Adefolaju, Adebimpe et al. “Informing development of brain cancer therapies within "preclinical trials" using ex vivo patient tumors.” Advanced drug delivery reviews vol. 228 (2026): 115736. doi:10.1016/j.addr.2025.115736

3. "Clinical Trial Failures - Losses of 2016." TrialX, 28 Mar. 2017, https://trialx.com/clinical-trial-failures-losses-of-2016/.



