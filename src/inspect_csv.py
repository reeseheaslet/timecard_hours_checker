from pathlib import Path
import pandas as pd
from loaders import load_csv


def inspect_dataframe(df: pd.DataFrame, label: str, rows: int = 5) -> None:
    """
    Print basic inspection information for a DataFrame.
    """
    print(f"\n{'=' * 60}")
    print(f"INSPECTING: {label}")
    print(f"{'=' * 60}")

    print("\n--- Shape ---")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n--- Columns ---")
    for col in df.columns:
        print(col)

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- First Rows ---")
    print(df.head(rows))

    print("\n--- Missing Values Per Column ---")
    print(df.isna().sum())


def inspect_csv(file_path: str, label: str, rows: int = 5) -> None:
    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {path}")
        return

    df = load_csv(file_path)
    inspect_dataframe(df, label=label, rows=rows)

if __name__ == "__main__":
    inspect_csv("data/raw/executime/executime_timecard.csv", label="executime")


    df = load_csv("data/raw/executime/executime_timecard.csv")

    print("\n--- Unique timeEntryTypeLabel values ---")
    print(df["timeEntryTypeLabel"].value_counts(dropna=False))

    print("\n--- Sample approvals values ---")
    print(df["approvals"].head(3).to_list())