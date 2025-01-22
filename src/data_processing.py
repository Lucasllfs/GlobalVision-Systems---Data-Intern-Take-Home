import pandas as pd
import sqlite3

# Load the data
accounts_file = "../data/accounts_anonymized.json"
support_cases_file = "../data/support_cases_anonymized.json"

accounts_df = pd.read_json(accounts_file)
support_cases_df = pd.read_json(support_cases_file)

# Save JSON files as CSV for easier usage later
accounts_df.to_csv("../data/accounts_anonymized.csv", index=False)
support_cases_df.to_csv("../data/support_cases_anonymized.csv", index=False)

# Reload data from CSV if needed
accounts_df = pd.read_csv("../data/accounts_anonymized.csv")
support_cases_df = pd.read_csv("../data/support_cases_anonymized.csv")

# Initial exploration
print("\n=== Accounts DataFrame ===")
print(accounts_df.info())
print(accounts_df.head())

print("\n=== Support Cases DataFrame ===")
print(support_cases_df.info())
print(support_cases_df.head())

# Connect to an SQLite database
conn = sqlite3.connect(":memory:")

# Save the DataFrames to SQLite
accounts_df.to_sql("accounts", conn, index=False, if_exists="replace")
support_cases_df.to_sql("support_cases", conn, index=False, if_exists="replace")

# Query 1: Industry performance overview
query_industry_performance = """
SELECT 
    a.account_industry, 
    COUNT(sc.case_sfid) AS total_cases, 
    SUM(CASE WHEN sc.case_status = 'Closed' THEN 1 ELSE 0 END) AS closed_cases, 
    ROUND(SUM(CASE WHEN sc.case_status = 'Closed' THEN 1 ELSE 0 END) * 100.0 / COUNT(sc.case_sfid), 2) AS closure_rate,
    AVG(JULIANDAY(sc.case_closed_date) - JULIANDAY(sc.case_created_date)) AS avg_resolution_time
FROM 
    accounts a
LEFT JOIN 
    support_cases sc
ON 
    a.account_sfid = sc.account_sfid
GROUP BY 
    a.account_industry
ORDER BY 
    total_cases DESC;
"""
result_industry_performance_df = pd.read_sql_query(query_industry_performance, conn)

# Query 2: Accounts with long resolution times
query_long_resolution_accounts = """
SELECT 
    a.account_name, 
    a.account_country, 
    AVG(JULIANDAY(sc.case_closed_date) - JULIANDAY(sc.case_created_date)) AS avg_resolution_time,
    COUNT(sc.case_sfid) AS total_cases
FROM 
    accounts a
LEFT JOIN 
    support_cases sc
ON 
    a.account_sfid = sc.account_sfid
WHERE 
    sc.case_closed_date IS NOT NULL
GROUP BY 
    a.account_name, a.account_country
HAVING 
    avg_resolution_time > 10
ORDER BY 
    avg_resolution_time DESC;
"""
result_long_resolution_accounts_df = pd.read_sql_query(query_long_resolution_accounts, conn)

# Query 3: Severity and priority correlation by industry
query_severity_priority = """
SELECT 
    a.account_industry, 
    sc.case_severity, 
    sc.case_priority, 
    COUNT(sc.case_sfid) AS case_count
FROM 
    accounts a
LEFT JOIN 
    support_cases sc
ON 
    a.account_sfid = sc.account_sfid
GROUP BY 
    a.account_industry, sc.case_severity, sc.case_priority
ORDER BY 
    a.account_industry, case_count DESC;
"""
result_severity_priority_df = pd.read_sql_query(query_severity_priority, conn)

# Query 4: Regional performance overview
query_region_performance = """
SELECT 
    a.account_country, 
    COUNT(sc.case_sfid) AS total_cases, 
    SUM(CASE WHEN sc.case_status = 'Closed' THEN 1 ELSE 0 END) AS closed_cases, 
    ROUND(SUM(CASE WHEN sc.case_status = 'Closed' THEN 1 ELSE 0 END) * 100.0 / COUNT(sc.case_sfid), 2) AS closure_rate
FROM 
    accounts a
LEFT JOIN 
    support_cases sc
ON 
    a.account_sfid = sc.account_sfid
GROUP BY 
    a.account_country
ORDER BY 
    total_cases DESC;
"""
result_region_performance_df = pd.read_sql_query(query_region_performance, conn)

# Query 5: Case creation trends over time
query_case_trends = """
SELECT 
    strftime('%Y-%m', sc.case_created_date) AS case_month, 
    COUNT(sc.case_sfid) AS total_cases
FROM 
    support_cases sc
GROUP BY 
    case_month
ORDER BY 
    case_month;
"""
result_case_trends_df = pd.read_sql_query(query_case_trends, conn)

# Display the results
print("\n=== Industry Performance Overview ===")
print(result_industry_performance_df)

print("\n=== Accounts with Long Resolution Times ===")
print(result_long_resolution_accounts_df)

print("\n=== Severity and Priority Correlation by Industry ===")
print(result_severity_priority_df)

print("\n=== Regional Performance Overview ===")
print(result_region_performance_df)

print("\n=== Case Creation Trends Over Time ===")
print(result_case_trends_df)

# Save the results to CSV files
result_industry_performance_df.to_csv("../data/industry_performance.csv", index=False)
result_long_resolution_accounts_df.to_csv("../data/long_resolution_accounts.csv", index=False)
result_severity_priority_df.to_csv("../data/severity_priority_correlation.csv", index=False)
result_region_performance_df.to_csv("../data/region_performance.csv", index=False)
result_case_trends_df.to_csv("../data/case_trends.csv", index=False)

conn.close()
