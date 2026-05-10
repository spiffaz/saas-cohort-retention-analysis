"""
Step 3 — Define user cohorts.
Each user's cohort is the calendar month of their first event (first_event_date).
Writes cohort_assignments.csv.
"""
import pandas as pd

# Load cleaned dataset — event_date is our timestamp column
df = pd.read_csv('saas_events_cleaned.csv')
df['event_timestamp'] = pd.to_datetime(df['event_date'], errors='coerce')

# Drop rows with unparseable or missing timestamps
before = len(df)
df = df.dropna(subset=['user_id', 'event_timestamp'])
dropped = before - len(df)
if dropped:
    print(f"Dropped {dropped} rows with missing user_id or timestamp")

# Find the first event timestamp for each unique user
first_events = (
    df.groupby('user_id')['event_timestamp']
    .min()
    .reset_index()
)
first_events.columns = ['user_id', 'first_event_date']

# Extract cohort month (YYYY-MM Period)
first_events['cohort_month'] = first_events['first_event_date'].dt.to_period('M')

# Merge cohort information back to main dataframe
df = df.merge(first_events[['user_id', 'cohort_month']], on='user_id')

print(first_events.head(10).to_string(index=False))
print(f"\nTotal users:   {len(first_events)}")
print(f"Total cohorts: {first_events['cohort_month'].nunique()}")
print("\nUsers per cohort:")
print(first_events['cohort_month'].value_counts().sort_index().to_string())

df.to_csv('cohort_assignments.csv', index=False)
print("\nSaved: cohort_assignments.csv")
