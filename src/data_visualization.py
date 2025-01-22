import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed data
industry_performance_file = "../data/industry_performance.csv"
long_resolution_accounts_file = "../data/long_resolution_accounts.csv"
severity_priority_file = "../data/severity_priority_correlation.csv"
region_performance_file = "../data/region_performance.csv"
case_trends_file = "../data/case_trends.csv"

industry_performance_df = pd.read_csv(industry_performance_file)
long_resolution_accounts_df = pd.read_csv(long_resolution_accounts_file)
severity_priority_df = pd.read_csv(severity_priority_file)
region_performance_df = pd.read_csv(region_performance_file)
case_trends_df = pd.read_csv(case_trends_file)

# Visual
sns.set_theme(style="whitegrid")

# Visualization 1: Industry Performance Overview
plt.figure(figsize=(12, 6))
sns.barplot(
    data=industry_performance_df, 
    x="account_industry", 
    y="total_cases", 
    palette="Blues_d"
)
plt.title("Total Cases by Industry", fontsize=16)
plt.xlabel("Industry", fontsize=12)
plt.ylabel("Total Cases", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../data/industry_performance_plot.png")
plt.show()

# Visualization 2: Case Trends Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=case_trends_df, 
    x="case_month", 
    y="total_cases", 
    marker="o", 
    color="b"
)
plt.title("Case Creation Trends Over Time", fontsize=16)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Cases", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../data/case_trends_plot.png")
plt.show()

# Visualization 3: Regional Performance Overview
plt.figure(figsize=(12, 6))
sns.barplot(
    data=region_performance_df, 
    x="account_country", 
    y="closure_rate", 
    palette="coolwarm"
)
plt.title("Closure Rate by Country", fontsize=16)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Closure Rate (%)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../data/region_performance_plot.png")
plt.show()

# Visualization 4: Severity and Priority Correlation
plt.figure(figsize=(14, 7))
severity_priority_pivot = severity_priority_df.pivot_table(
    values="case_count", index="case_priority", columns="case_severity"
)
sns.heatmap(
    severity_priority_pivot, 
    annot=True, 
    fmt=".0f", 
    cmap="YlGnBu", 
    cbar_kws={'label': 'Case Count'}
)
plt.title("Case Severity and Priority Correlation", fontsize=16)
plt.xlabel("Severity", fontsize=12)
plt.ylabel("Priority", fontsize=12)
plt.tight_layout()
plt.savefig("../data/severity_priority_correlation_plot.png")
plt.show()

# Visualization 5: Accounts with Long Resolution Times
plt.figure(figsize=(12, 6))
sns.barplot(
    data=long_resolution_accounts_df.head(10), 
    x="account_name", 
    y="avg_resolution_time", 
    palette="Reds_d"
)
plt.title("Top 10 Accounts by Average Resolution Time", fontsize=16)
plt.xlabel("Account Name", fontsize=12)
plt.ylabel("Average Resolution Time (days)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../data/long_resolution_accounts_plot.png")
plt.show()
