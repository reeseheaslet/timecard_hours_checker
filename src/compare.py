import pandas as pd


def compare_firstdue_vs_executime(
    firstdue_df: pd.DataFrame,
    executime_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare First Due vs executime on:
    - EmpKey
    - WorkDate
    - NormalizedType

    Produces a simple mismatch table.
    """

    fd = firstdue_df.copy()
    et = executime_df.copy()

    fd = fd.rename(columns={"Hours": "FD_Hours"})
    et = et.rename(columns={"Hours": "ET_Hours"})

    # Keep only needed columns
    fd = fd[["EmpKey", "WorkDate", "NormalizedType", "FD_Hours"]]
    et = et[["EmpKey", "WorkDate", "NormalizedType", "ET_Hours"]]

    merged = pd.merge(
        fd,
        et,
        on=["EmpKey", "WorkDate", "NormalizedType"],
        how="outer",
    )

    # Fill missing with 0 for comparison
    merged["FD_Hours"] = merged["FD_Hours"].fillna(0)
    merged["ET_Hours"] = merged["ET_Hours"].fillna(0)

    
    merged["HourDiff"] = merged["FD_Hours"] - merged["ET_Hours"]
# Tolerance set to 0.15 hours because First Due rounds in 0.5-hour increments.
# This suppresses tiny float/rounding noise while still catching meaningful mismatches.
    merged["IsMismatch"] = merged["HourDiff"].abs() > 0.15

    merged = merged.sort_values(
        by=["EmpKey", "WorkDate", "NormalizedType"]
    ).reset_index(drop=True)

    return merged