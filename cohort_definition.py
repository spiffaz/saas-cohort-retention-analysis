"""
Step 3 — Define user cohorts.
Each user's cohort is the calendar month of their first recorded event.
Writes cohort_assignments.csv.
"""
import pandas as pd

df = pd.read_csv('saas_events_cleaned.csv', parse_dates=['event_date'])
df['event_month'] = df['event_date'].dt.to_period('M')

# First event month per user — that is their cohort
first_event = (
    df.groupby('user_id')['event_month']
    .min()
    .rename('cohort_month')
    .reset_index()
)

df = df.merge(first_event, on='user_id')

print("=== Cohort Assignments ===")
print(f"Total users: {df['user_id'].nunique()}")
print(f"Total cohorts: {df['cohort_month'].nunique()}")
print("\nUsers per cohort:")
cohort_sizes = first_event['cohort_month'].value_counts().sort_index()
print(cohort_sizes.to_string())

df.to_csv('cohort_assignments.csv', index=False)
print("\nSaved: cohort_assignments.csv")
