# Netflix Customer Churn & Engagement Analytics

A Python + SQL data pipeline that loads a Netflix-style customer dataset into
a SQLite database, analyses it with SQL queries, and visualises churn
patterns with pandas and matplotlib.

## What this project does

1. **Loads** a 5,000-row customer dataset (`netflix_customer_churn.csv`) into
   a SQLite database using `pandas` and `sqlite3`.
2. **Queries** the database with SQL to summarise churn by subscription
   type, region, viewing behaviour, and favourite genre.
3. **Visualises** the results as bar charts saved as PNG files, using
   `matplotlib`.

The goal is to practise moving data between a flat file, a relational
database, and analysis/plotting tools — the kind of basic data pipeline
used in real analytics and placement-style data tasks.

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3 | Core scripting language |
| pandas | Reading the CSV, running SQL queries, shaping results |
| sqlite3 (standard library) | Lightweight relational database |
| matplotlib | Generating chart images |

## Dataset

`netflix_customer_churn.csv` — 5,000 customer records with columns:

`customer_id, age, gender, subscription_type, watch_hours, last_login_days, region, device, monthly_fee, churned, payment_method, number_of_profiles, avg_watch_time_per_day, favorite_genre`

## Project structure

```
netflix-churn-analysis/
├── load_data.py                       # CSV -> SQLite
├── analysis.py                        # SQL queries + chart generation
├── netflix_customer_churn.csv         # raw dataset
├── requirements.txt                   # Python dependencies
├── chart_churn_by_subscription.png
├── chart_churn_by_region.png
├── chart_watch_hours_vs_churn.png
├── chart_churn_by_genre.png
└── README.md
```

`netflix_stats.db` is generated automatically when you run `load_data.py`
and is not committed to the repo (see `.gitignore`).

## Setup

```bash
git clone <your-repo-url>
cd netflix-churn-analysis

python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

**1. Load the CSV into SQLite:**

```bash
python load_data.py
```

Creates `netflix_stats.db` with a single table, `netflix_churn`.

**2. Run the analysis:**

```bash
python analysis.py
```

Prints summary tables to the console and (re)generates the four chart PNGs
in the project folder.

## Example findings

- Overall churn rate across all customers: **~50%**
- **Basic** subscribers churn at a noticeably higher rate (~62%) than
  **Standard** (~45%) or **Premium** (~44%) subscribers
- Churned customers watch far fewer hours on average (5.9 vs 17.5 hours)
  and go quiet for roughly twice as long before leaving
- Churn rate varies only slightly by region and favourite genre — tier and
  engagement level matter far more than demographics or content taste


## Possible extensions

- Train a simple classifier (e.g. logistic regression) to predict churn
- Add a Jupyter notebook for interactive exploration
- Parameterise `analysis.py` to accept different group-by columns via CLI args
