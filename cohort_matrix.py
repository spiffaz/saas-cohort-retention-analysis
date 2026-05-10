"""
Step 5 — Build the cohort matrix.
Rows = cohort month, columns = months since first event (cohort index).
Cell value = distinct active users in that cohort at that age.
Writes cohort_matrix.csv.
"""
import pandas as pd

df = pd.read_csv('cohort_with_index.csv')

cohort_data = (
    df.groupby(['cohort_month', 'cohort_index'])['user_id']
    .nunique()
    .reset_index()
    .rename(columns={'user_id': 'active_users'})
)

cohort_matrix = cohort_data.pivot_table(
    index='cohort_month',
    columns='cohort_index',
    values='active_users'
)

print("=== Cohort Matrix (active user counts) ===")
print(cohort_matrix.to_string())

cohort_matrix.to_csv('cohort_matrix.csv')
print("\nSaved: cohort_matrix.csv")
