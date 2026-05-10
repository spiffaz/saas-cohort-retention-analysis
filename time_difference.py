"""
Step 4 — Calculate time difference in months between each event and the user's first event.
Adds cohort_index column (0 = same month as first event, 1 = one month later, etc.).
Writes cohort_with_index.csv.
"""
import pandas as pd

df = pd.read_csv('cohort_assignments.csv')

# Restore Period dtype after CSV round-trip
df['event_month']  = df['event_date'].apply(lambda d: pd.Period(d[:7], 'M'))
df['cohort_month'] = df['cohort_month'].apply(lambda d: pd.Period(d, 'M'))

# Months since first event
df['cohort_index'] = (df['event_month'] - df['cohort_month']).apply(lambda x: x.n)

print("=== Cohort Index Distribution ===")
print(df['cohort_index'].value_counts().sort_index().to_string())

print(f"\nMax cohort age observed: {df['cohort_index'].max()} months")
print("\nSample rows:")
print(df[['user_id', 'event_date', 'event_type', 'cohort_month', 'cohort_index']].head(10).to_string(index=False))

df.to_csv('cohort_with_index.csv', index=False)
print("\nSaved: cohort_with_index.csv")
