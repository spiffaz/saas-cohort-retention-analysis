"""
Step 2 — Data cleaning and preprocessing.
Reads user_events.csv, validates and cleans it, writes saas_events_cleaned.csv.
"""
import pandas as pd
import numpy as np

RAW_FILE     = 'user_events.csv'
CLEANED_FILE = 'saas_events_cleaned.csv'

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_FILE)

print("=== Initial dataset ===")
print("Shape:", df.shape)
print("\nColumn data types:")
print(df.dtypes)
print("\nMissing values per column:")
print(df.isnull().sum())

# ---------------------------------------------------------------------------
# Convert timestamps
# ---------------------------------------------------------------------------
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
unparseable = df['event_date'].isnull().sum()
if unparseable:
    print(f"\nWarning: {unparseable} rows with unparseable dates — will be dropped")

# ---------------------------------------------------------------------------
# Drop rows missing critical columns
# ---------------------------------------------------------------------------
critical_columns = ['user_id', 'event_date', 'event_type']
initial_count = len(df)

df = df.dropna(subset=critical_columns)
rows_dropped = initial_count - len(df)
print(f"\nRows dropped due to missing critical data: {rows_dropped}")

# ---------------------------------------------------------------------------
# Normalise string columns
# ---------------------------------------------------------------------------
df['user_id']    = df['user_id'].astype(str).str.strip()
df['event_type'] = df['event_type'].astype(str).str.strip().str.lower()

# Remove any duplicate events (same user + date + type)
before_dedup = len(df)
df = df.drop_duplicates(subset=['user_id', 'event_date', 'event_type'])
dupes_removed = before_dedup - len(df)
print(f"Duplicate rows removed: {dupes_removed}")

# ---------------------------------------------------------------------------
# Add derived columns used in downstream steps
# ---------------------------------------------------------------------------
df['event_month'] = df['event_date'].dt.to_period('M')

# ---------------------------------------------------------------------------
# Verify final dtypes
# ---------------------------------------------------------------------------
print("\n=== Cleaned dataset ===")
print("Shape:", df.shape)
print("\nData types after cleaning:")
# user_id: object (str), event_date: datetime64, event_type: object, event_month: period
print(df.dtypes)
print("\nNull counts after cleaning:")
print(df.isnull().sum())
print("\nEvent type distribution:")
print(df['event_type'].value_counts())
print("\nFirst 5 rows:")
print(df.head())

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
df.to_csv(CLEANED_FILE, index=False)
print(f"\nSaved cleaned dataset to '{CLEANED_FILE}'")
