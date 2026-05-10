"""
Step 7 — Visualise retention curves.
Produces three charts saved as PNG files.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

sns.set_theme(style='whitegrid', palette='muted')

retention_pct = pd.read_csv('retention_rates.csv', index_col=0)
retention_pct.columns = retention_pct.columns.astype(int)

# ---------------------------------------------------------------------------
# Chart 1: Heatmap
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(
    retention_pct.round(1),
    annot=True, fmt='.1f',
    cmap='YlOrRd_r',
    linewidths=0.5,
    vmin=0, vmax=100,
    ax=ax
)
ax.set_title('Monthly Cohort Retention Rate (%)', fontsize=14, pad=12)
ax.set_xlabel('Months since first event')
ax.set_ylabel('Cohort (first event month)')
ax.set_yticklabels(retention_pct.index, rotation=0)
plt.tight_layout()
plt.savefig('cohort_heatmap.png', dpi=150)
plt.close()
print("Saved: cohort_heatmap.png")

# ---------------------------------------------------------------------------
# Chart 2: Retention curves — one line per cohort
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
for cohort, row in retention_pct.iterrows():
    row_clean = row.dropna()
    ax.plot(row_clean.index, row_clean.values, marker='o', markersize=4, linewidth=1.5, label=str(cohort))

ax.set_title('Retention Curves by Cohort', fontsize=14)
ax.set_xlabel('Months since first event')
ax.set_ylabel('Retention rate')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.legend(title='Cohort', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig('retention_curves.png', dpi=150)
plt.close()
print("Saved: retention_curves.png")

# ---------------------------------------------------------------------------
# Chart 3: Average retention across all cohorts
# ---------------------------------------------------------------------------
avg_retention = retention_pct.mean()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(avg_retention.index, avg_retention.values, marker='o', linewidth=2, color='steelblue')
ax.fill_between(avg_retention.index, avg_retention.values, alpha=0.15, color='steelblue')
ax.set_title('Average Retention Curve (all cohorts)', fontsize=14)
ax.set_xlabel('Months since first event')
ax.set_ylabel('Average retention rate')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set_ylim(0, 105)
for i, v in avg_retention.items():
    ax.annotate(f'{v:.1f}%', (i, v), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('avg_retention_curve.png', dpi=150)
plt.close()
print("Saved: avg_retention_curve.png")
