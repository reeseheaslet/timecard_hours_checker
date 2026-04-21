from pipeline import run_web_pipeline

result = run_web_pipeline(
    "data/raw/executime/executime_timecard.csv",
    "data/raw/firstdue/firstdue_timecard.csv",
    "2026-03-16",
    "2026-03-29",
)

print(result)
print("\n--- MISMATCHES ONLY ---")
print(result[result["IsMismatch"]])