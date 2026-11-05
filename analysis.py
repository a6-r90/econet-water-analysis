"""Portfolio refactor of ECONET's water-data analysis notebook."""
from pathlib import Path
import argparse
import pandas as pd

REQUIRED = ["Characteristic Name", "Result Value", "Result Unit"]

def load_data(source):
    """Read CSV or Excel and validate the water-measurement schema."""
    name = getattr(source, "name", str(source)).lower()
    if name.endswith(".csv"):
        data = pd.read_csv(source)
    elif name.endswith(".xlsx"):
        data = pd.read_excel(source)
    else:
        raise ValueError("Use a CSV or .xlsx file.")
    missing = set(REQUIRED) - set(data.columns)
    if missing:
        raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
    data = data.copy()
    for col in ["Characteristic Name", "Result Unit"]:
        data[col] = data[col].astype("string").str.strip().replace("", pd.NA)
    # Do not turn censored measurements such as '<0.1' into exact readings.
    data["Result Value"] = pd.to_numeric(data["Result Value"], errors="coerce")
    data = data.dropna(subset=REQUIRED)
    data = data[data["Result Value"].abs() != float("inf")]
    if data.empty:
        raise ValueError("No valid numeric measurements with names and units remain.")
    if "Activity Start Date" in data:
        data["Activity Start Date"] = pd.to_datetime(data["Activity Start Date"], errors="coerce")
    return data

def summarise(data):
    """Keep units separate; values are descriptive, not pollution rankings."""
    return (data.groupby(["Characteristic Name", "Result Unit"])["Result Value"]
            .agg(sample_count="count", mean="mean", minimum="min", maximum="max")
            .reset_index())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    data = load_data(args.file)
    summary = summarise(data)
    args.output.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.output / "cleaned_data.csv", index=False)
    summary.to_csv(args.output / "summary.csv", index=False)
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
