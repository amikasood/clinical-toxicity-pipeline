# Clinical Toxicity Pipeline

Starter Python project scaffold for building data and modeling pipelines.

## Quick start (PowerShell)

```powershell
cd c:\amika\personal\AI_ML\clinical-toxicity-pipeline
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
clinical-toxicity --dataset tox21
pytest
```

## Project structure

```text
clinical-toxicity-pipeline/
  pyproject.toml
  requirements.txt
  README.md
  src/
    clinical_toxicity_pipeline/
      __init__.py
      main.py
  tests/
    test_main.py
```

## What to add next

- Add data ingestion code under `src/clinical_toxicity_pipeline/`.
- Add configuration handling (`.env`, YAML, or argparse subcommands).
- Add notebooks in a separate `notebooks/` folder if needed.
- Expand tests as you add pipeline stages.
