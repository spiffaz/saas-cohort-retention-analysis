"""
Step 6 — Calculate retention rates.
Divides each cohort row by the month-0 cohort size to produce percentages.
Writes retention_rates.csv.
"""
import pandas as pd

cohort_matrix = pd.read_csv('cohort_matrix.csv', index_col=0)
cohort_matrix.columns = cohort_matrix.columns.astype(int)

cohort_sizes  = cohort_matrix[0]
retention_pct = cohort_matrix.divide(cohort_sizes, axis=0).multiply(100).round(2)

print("=== Cohort sizes (month 0) ===")
print(cohort_sizes.to_string())

print("\n=== Retention rates (%) ===")
print(retention_pct.to_string())

avg = retention_pct.mean().round(2)
print("\n=== Average retention across cohorts ===")
for month, rate in avg.items():
    print(f"  Month {month:2d}: {rate:.1f}%")

if 1 in avg.index:
    drop = avg[0] - avg[1]
    print(f"\nMonth-0 to Month-1 drop-off: {drop:.1f} pp  ({drop / avg[0] * 100:.1f}% of month-0 users lost)")

retention_pct.to_csv('retention_rates.csv')
print("\nSaved: retention_rates.csv")
