"""
Steps 4-6: time difference calculation, cohort matrix, and retention rates.

Columns produced:
  event_month          — Period[M] of the event
  cohort_age           — months since the user's cohort month (DoD step 4)
  cohort_period_number — alias for cohort_age used in pivot (DoD steps 4/5)

Outputs:
  cohort_matrix.csv    — active user counts (step 5)
  retention_rates.csv  — retention percentages (step 6)
"""
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Load — use cleaned data with cohort_month already merged
# ---------------------------------------------------------------------------
df = pd.read_csv('cohort_assignments.csv')
df['event_timestamp'] = pd.to_datetime(df['event_date'], errors='coerce')
df = df.dropna(subset=['user_id', 'event_timestamp', 'event_type'])

# Restore Period columns after CSV round-trip
df['event_month']  = df['event_timestamp'].dt.to_period('M')
df['cohort_month'] = df['cohort_month'].apply(lambda v: pd.Period(v, 'M'))

# ---------------------------------------------------------------------------
# Step 4 — Calculate months elapsed since cohort month
# ---------------------------------------------------------------------------
df['cohort_age']           = (df['event_month'] - df['cohort_month']).apply(lambda x: x.n)
df['cohort_period_number'] = df['cohort_age']   # same value, matches step-5 pivot name

# Verify: all values non-negative integers starting at 0
assert df['cohort_age'].min() >= 0, "Negative cohort_age found"
print("Step 4 — cohort_age sample:")
print(df[['user_id', 'event_timestamp', 'cohort_month', 'event_month', 'cohort_age']].head(10).to_string(index=False))
print(f"\ncohort_age range: {df['cohort_age'].min()} to {df['cohort_age'].max()}")
print(f"event_month dtype: {df['event_month'].dtype}")
print(f"cohort_age dtype:  {df['cohort_age'].dtype}")

# ---------------------------------------------------------------------------
# Step 5 — Cohort matrix (unique users per cohort per period)
# ---------------------------------------------------------------------------
cohort_counts = (
    df.groupby(['cohort_month', 'cohort_period_number'])
    .agg(user_count=('user_id', 'nunique'))
    .reset_index()
)

cohort_matrix = cohort_counts.pivot(
    index='cohort_month',
    columns='cohort_period_number',
    values='user_count'
)

print("\nStep 5 — Cohort matrix (active user counts):")
print(cohort_matrix)
print(f"\nMatrix shape: {cohort_matrix.shape}")

cohort_matrix.to_csv('cohort_matrix.csv')
print("Saved: cohort_matrix.csv")

# ---------------------------------------------------------------------------
# Step 6 — Retention rates
# ---------------------------------------------------------------------------
# Initial cohort size = period-0 column
cohort_sizes     = cohort_matrix.iloc[:, 0]
retention_matrix = cohort_matrix.divide(cohort_sizes, axis=0)

# Verify period-0 column is all 1.0
assert (retention_matrix.iloc[:, 0].dropna() == 1.0).all(), "Period-0 column is not all 1.0"

retention_pct = retention_matrix * 100

print("\nStep 6 — Retention matrix (%):")
print(retention_pct.round(2))

print("\nVerification — period-0 column (should all be 1.0 / 100%):")
print(retention_matrix.iloc[:, 0].to_string())

avg = retention_pct.mean()
print("\nAverage retention across cohorts:")
for period, rate in avg.items():
    print(f"  Period {period:2d}: {rate:.1f}%")

retention_pct.to_csv('retention_rates.csv')
print("\nSaved: retention_rates.csv")
