"""
load_data.py
Reads the Netflix customer churn CSV and loads it into a SQLite database.
"""

import os
import sqlite3
import pandas as pd

# Resolve paths relative to this script's own location, so it works
# no matter which folder the script is run from.
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "netflix_customer_churn.csv")
db_path = os.path.join(script_dir, "netflix_stats.db")

# Read CSV and connect to (or create) the database
df = pd.read_csv(csv_path)
conn = sqlite3.connect(db_path)

# Write dataframe straight into a SQL table
df.to_sql("netflix_churn", conn, if_exists="replace", index=False)
conn.close()
print("Data loaded into netflix_stats.db")
