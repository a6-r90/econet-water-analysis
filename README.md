# ECONET — Water Data Analysis

ECONET was a team smart-agriculture hackathon project. My contribution focused on programming and data analysis in Python. This repository presents the water-measurement analysis component, not a completed AI or IoT deployment.

## Included
- `analysis.py`: read CSV/Excel, validate columns, clean numeric observations and summarise by characteristic **and unit**.
- `app.py`: Streamlit explorer with location filters, a distribution plot and dated measurements.
- `notebooks/water_analysis.ipynb`: concise notebook using the same analysis functions.
- `data/example.csv`: tiny, explicitly synthetic example for trying the interface.

## Run
Use Python 3.10+ in a virtual environment:
```bash
python -m pip install -r requirements.txt
python analysis.py data/example.csv
python -m streamlit run app.py
```
Upload `data/example.csv` in the dashboard, or supply your own appropriately licensed data.

Required columns: `Characteristic Name`, `Result Value`, `Result Unit`.
Optional: `Activity Start Date`, `Monitoring Location Name`, `Monitoring Location State`.

## Portfolio editing notes
This version was refactored from the project's `PROJECT.ipynb`. Duplicate experiments, invalid local paths, embedded outputs and ngrok setup were removed. A local upload interface replaces fixed filenames. Summary grouping now keeps units separate; high numerical values are not described as the most polluted measurements.

These are later portfolio edits, not claims about features delivered during the hackathon. The source was reviewed, but this edited version has not yet been executed in a Python environment. Dependencies are unpinned until runtime verification.

## Interpretation
Only exact numeric readings are included: censored values such as `<0.1`, missing units and invalid readings are dropped. Counts refer to retained rows. Units are not converted or normalised, sampling imbalance can affect averages, and records may span different sites and dates. This is exploratory analysis, not a water-safety assessment. The bundled data is synthetic and demonstrates no real environmental finding.
