import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import textwrap
from matplotlib.ticker import FixedLocator

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

# Set style and colors for the dashboard
sns.set_theme(style="whitegrid")
primary_color = "#d90429"  # Red
secondary_color = "#2b2b2b"  # Black
background_color = "#ffffff"  # White

# Create a figure for the dashboard
plt.figure(figsize=(16, 12), facecolor=background_color)
gs = GridSpec(3, 2, figure=plt.gcf(), wspace=0.5, hspace=1.5)

# Visualization 1: Total Cases by Industry
ax1 = plt.subplot(gs[0, 0])
sns.barplot(
    data=industry_performance_df, 
    x="account_industry", 
    y="total_cases", 
    hue="account_industry",  
    palette=[primary_color] * industry_performance_df["account_industry"].nunique(),  
    legend=False  
, ax=ax1)
ax1.set_title("Total Cases by Industry", fontsize=14, color=secondary_color)
ax1.set_xlabel("Industry", fontsize=12, color=secondary_color)
ax1.set_ylabel("Total Cases", fontsize=12, color=secondary_color)
ax1.tick_params(colors=secondary_color)
labels = [textwrap.shorten(label.get_text(), width=15, placeholder="...") for label in ax1.get_xticklabels()]
ax1.set_xticks(ax1.get_xticks())  
ax1.set_xticklabels(labels, rotation=45, ha="right")

# Visualization 2: Case Creation Trends Over Time
ax2 = plt.subplot(gs[0, 1])
sns.lineplot(
    data=case_trends_df, 
    x="case_month", 
    y="total_cases", 
    marker="o", 
    color=primary_color
, ax=ax2)
ax2.set_title("Case Creation Trends Over Time", fontsize=14, color=secondary_color)
ax2.set_xlabel("Month", fontsize=12, color=secondary_color)
ax2.set_ylabel("Total Cases", fontsize=12, color=secondary_color)
ax2.tick_params(colors=secondary_color)
ax2.set_xticks(ax2.get_xticks())  
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

# Visualization 3: Top 10 Accounts by Average Resolution Time
ax3 = plt.subplot(gs[1, 0])
sns.barplot(
    data=long_resolution_accounts_df.head(10), 
    x="account_name", 
    y="avg_resolution_time", 
    hue="account_name",  
    palette=[primary_color] * long_resolution_accounts_df.head(10)["account_name"].nunique(),  
    legend=False  
, ax=ax3)
ax3.set_title("Top 10 Accounts by Average Resolution Time", fontsize=14, color=secondary_color)
ax3.set_xlabel("Account Name", fontsize=12, color=secondary_color)
ax3.set_ylabel("Average Resolution Time (days)", fontsize=12, color=secondary_color)
ax3.tick_params(colors=secondary_color)
ax3.set_xticks(ax3.get_xticks())  
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")

# Visualization 4: Severity and Priority Correlation
ax5 = plt.subplot(gs[1, 1])
severity_priority_pivot = severity_priority_df.pivot_table(
    values="case_count", index="case_priority", columns="case_severity"
)
sns.heatmap(
    severity_priority_pivot, 
    annot=True, 
    fmt=".0f", 
    cmap="Reds", 
    cbar_kws={'label': 'Case Count'},
    ax=ax5
)
ax5.set_title("Case Severity and Priority Correlation", fontsize=14, color=secondary_color)
ax5.set_xlabel("Severity", fontsize=12, color=secondary_color)
ax5.set_ylabel("Priority", fontsize=12, color=secondary_color)

# Visualization 5: Closure Rate by Country
ax4 = plt.subplot(gs[2, :])
sns.barplot(
    data=region_performance_df, 
    x="account_country", 
    y="closure_rate", 
    hue="account_country",  
    palette=[primary_color] * region_performance_df["account_country"].nunique(),  
    legend=False  
, ax=ax4)
ax4.set_title("Closure Rate by Country", fontsize=14, color=secondary_color)
ax4.set_xlabel("Country", fontsize=12, color=secondary_color)
ax4.set_ylabel("Closure Rate (%)", fontsize=12, color=secondary_color)
ax4.tick_params(colors=secondary_color)
ax4.set_xticks(ax4.get_xticks())  
ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha="right")

logo = plt.imread("../assets/logo.jpg")  
new_ax = plt.gcf().add_axes([0.9, 0.9, 0.1, 0.1], anchor='NE', zorder=1)
new_ax.imshow(logo)
new_ax.axis("off")

# Save the dashboard as a single image
plt.savefig("../data/dashboard.png", dpi=300, facecolor=background_color)
plt.show()