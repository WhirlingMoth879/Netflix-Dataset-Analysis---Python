"""
analysis.py
Runs SQL queries against netflix_stats.db and produces summary charts
using pandas + matplotlib.
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "netflix_stats.db")

conn = sqlite3.connect(db_path)

# 1. Overall churn rate
overall = pd.read_sql_query("""
    SELECT
        COUNT(*) AS total_customers,
        SUM(churned) AS churned_customers,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) AS churn_rate_pct
    FROM netflix_churn
""", conn)
print("\n=== Overall churn rate ===")
print(overall)


# 2. Churn rate by subscription type
by_subscription = pd.read_sql_query("""
    SELECT
        subscription_type,
        COUNT(*) AS customers,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) AS churn_rate_pct
    FROM netflix_churn
    GROUP BY subscription_type
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n=== Churn rate by subscription type ===")
print(by_subscription)


# 3. Churn rate by region
by_region = pd.read_sql_query("""
    SELECT
        region,
        COUNT(*) AS customers,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) AS churn_rate_pct
    FROM netflix_churn
    GROUP BY region
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n=== Churn rate by region ===")
print(by_region)


# 4. Average watch hours: churned vs retained
watch_vs_churn = pd.read_sql_query("""
    SELECT
        churned,
        ROUND(AVG(watch_hours), 2) AS avg_watch_hours,
        ROUND(AVG(avg_watch_time_per_day), 2) AS avg_daily_watch_time,
        ROUND(AVG(last_login_days), 2) AS avg_days_since_login
    FROM netflix_churn
    GROUP BY churned
""", conn)
print("\n=== Watch behaviour: churned (1) vs retained (0) ===")
print(watch_vs_churn)


# 5. Churn rate by favourite genre
by_genre = pd.read_sql_query("""
    SELECT
        favorite_genre,
        COUNT(*) AS customers,
        ROUND(100.0 * SUM(churned) / COUNT(*), 2) AS churn_rate_pct
    FROM netflix_churn
    GROUP BY favorite_genre
    ORDER BY churn_rate_pct DESC
""", conn)
print("\n=== Churn rate by favourite genre ===")
print(by_genre)

conn.close()

# =================================================================
# Charts
# =================================================================

# Chart 1: Churn rate by subscription type
plt.figure(figsize=(6, 4))
plt.bar(by_subscription["subscription_type"], by_subscription["churn_rate_pct"], color="#E50914")
plt.title("Churn Rate by Subscription Type")
plt.xlabel("Subscription Type")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "chart_churn_by_subscription.png"))
plt.close()

# Chart 2: Churn rate by region
plt.figure(figsize=(7, 4))
plt.bar(by_region["region"], by_region["churn_rate_pct"], color="#221f1f")
plt.title("Churn Rate by Region")
plt.xlabel("Region")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "chart_churn_by_region.png"))
plt.close()

# Chart 3: Average watch hours, churned vs retained
plt.figure(figsize=(5, 4))
labels = ["Retained", "Churned"]
plt.bar(labels, watch_vs_churn["avg_watch_hours"], color=["#2ca02c", "#E50914"])
plt.title("Average Watch Hours: Retained vs Churned")
plt.ylabel("Avg Watch Hours")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "chart_watch_hours_vs_churn.png"))
plt.close()

# Chart 4: Churn rate by favourite genre
plt.figure(figsize=(8, 4))
plt.bar(by_genre["favorite_genre"], by_genre["churn_rate_pct"], color="#564d4d")
plt.title("Churn Rate by Favourite Genre")
plt.xlabel("Genre")
plt.ylabel("Churn Rate (%)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(script_dir, "chart_churn_by_genre.png"))
plt.close()

print("\nCharts saved: chart_churn_by_subscription.png, chart_churn_by_region.png, "
      "chart_watch_hours_vs_churn.png, chart_churn_by_genre.png")
