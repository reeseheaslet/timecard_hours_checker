from loaders import load_executime_csv, load_firstdue_csv
from normalizers import (
    normalize_executime,
    normalize_firstdue,
    expand_firstdue_to_calendar_days,
    aggregate_firstdue_calendar_days,
    aggregate_executime_daily,
)
from compare import compare_firstdue_vs_executime
from pay_period import PAY_PERIOD_END, PAY_PERIOD_START, filter_to_pay_period


def main() -> None:
    print(
        "\n--- PAY PERIOD (inclusive) "
        f"{PAY_PERIOD_START:%m/%d/%Y} through {PAY_PERIOD_END:%m/%d/%Y} ---"
    )

    # executime
    executime_raw = load_executime_csv("data/raw/executime/executime_timecard.csv")
    executime_normalized = normalize_executime(executime_raw)
    executime_aggregated = aggregate_executime_daily(executime_normalized)

    print("\n--- NORMALIZED EXECUTIME DATA ---")
    print(executime_normalized)

    print("\n--- NORMALIZED EXECUTIME TYPE COUNTS ---")
    print(executime_normalized["NormalizedType"].value_counts(dropna=False))

    #### DEBUGGING ONLY! ####
    print("\n--- EXECUTIME RAW TYPE LABELS UNIQUE VALUES ---")
    print(executime_normalized["RawTypeLabel"].unique())

    # First Due
    firstdue_raw = load_firstdue_csv("data/raw/firstdue/firstdue_timecard.csv")
    firstdue_normalized = normalize_firstdue(firstdue_raw)
    firstdue_expanded = expand_firstdue_to_calendar_days(firstdue_raw)
    firstdue_aggregated = aggregate_firstdue_calendar_days(firstdue_expanded)

    n_fd = len(firstdue_aggregated)
    n_et = len(executime_aggregated)
    firstdue_for_compare = filter_to_pay_period(firstdue_aggregated)
    executime_for_compare = filter_to_pay_period(executime_aggregated)

    print(
        f"\n--- PAY PERIOD FILTER ---\n"
        f"First Due rows: {n_fd} -> {len(firstdue_for_compare)} "
        f"(dropped {n_fd - len(firstdue_for_compare)} outside period)\n"
        f"Executime rows: {n_et} -> {len(executime_for_compare)} "
        f"(dropped {n_et - len(executime_for_compare)} outside period)"
    )

    # Exclude Chief / or any other personnel from comparison
    EXCLUDED_EMPLOYEES = {
        "SWANSON, PAUL",
        "SANDHOLDT, PATRICK",
        "HOUCK, REBEKAH",
        "HUNTER, RACHEL",
        "KENUI, THERESA",
    }

    firstdue_for_compare = firstdue_for_compare[
        ~firstdue_for_compare["EmpKey"].isin(EXCLUDED_EMPLOYEES)
    ].copy()

    executime_for_compare = executime_for_compare[
        ~executime_for_compare["EmpKey"].isin(EXCLUDED_EMPLOYEES)
    ].copy()

    comparison = compare_firstdue_vs_executime(
        firstdue_for_compare,
        executime_for_compare,
    )

    print("\n--- NORMALIZED FIRST DUE (RAW INTERVALS) ---")
    print(firstdue_normalized)

    print("\n--- EXPANDED FIRST DUE (CALENDAR DAYS) ---")
    print(firstdue_expanded)

    print("\n--- AGGREGATED FIRST DUE (DAILY TOTALS) ---")
    print(firstdue_aggregated)

    print("\n--- AGGREGATED FIRST DUE TYPE COUNTS ---")
    print(firstdue_aggregated["NormalizedType"].value_counts(dropna=False))

    print("\n--- COMPARISON (FIRST DUE VS EXECUTIME) ---")
    print(comparison)

    ### DEBUGGING ONLY! ####
    print("\n--- AGGREGATED EXECUTIME (DAILY TOTALS) ---")
    print(executime_aggregated)

    print("\n--- AGGREGATED EXECUTIME TYPE COUNTS ---")
    print(executime_aggregated["NormalizedType"].value_counts(dropna=False))

    print("\n--- FIRST DUE RAW TYPE LABELS UNIQUE VALUES ---")
    print(firstdue_normalized["RawTypeLabel"].unique())

    print("\n--- MISMATCHES ONLY ---")
    print(comparison[comparison["IsMismatch"]])


if __name__ == "__main__":
    main()