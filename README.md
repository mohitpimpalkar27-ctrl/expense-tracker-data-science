# Expense Tracker App using Data Science

A reproducible portfolio project combining synthetic financial data, Python/Pandas analytics, monthly budgets, rule-based insights, Matplotlib reports, SQLite manual-entry storage, and a Streamlit dashboard.

**All bundled sample transactions are synthetic.** No real bank records are needed.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python run_analysis.py
python -m pytest -q
streamlit run main.py
```

## Dataset

`transaction_id,date,category,description,amount,payment_method,source`.

The 2,000 simulated transactions span 2025; a fixed random seed makes them reproducible. Rent is included once per month. Q4 has an illustrative spending uplift. These are assumptions, not observed financial behavior.

## App pages

Dashboard, Manage Expenses (SQLite CRUD), Analytics, Budget Planner, Insights. Choose between synthetic demo, manual records, and CSV upload. The date/category filters affect dashboard calculations. Budgets are **monthly**.

## CLI outputs

`python run_analysis.py` writes cleaned/processed CSV files, summary reports, and four PNG charts in `images/`.

## Financial formulas

- Total expense: sum(amount)
- Category share: category expense / total expense × 100
- Budget variance: budget − actual (negative means over budget)
- Utilization: actual / budget × 100 (undefined if budget is zero)
- MoM change: (current − previous) / previous × 100 (undefined if previous is zero)

## Limitations

This is a single-user, local educational application, not banking software. Manual data lives in a local SQLite file and is ignored by Git. The default budgets are illustrative and not personalized. Insights are rule-based, not machine learning or financial advice. Uploaded CSV data is analyzed in the session, not persisted to the database.

## Tests

`python -m pytest -q`

## Suggested GitHub proof

Screenshots: dashboard KPIs, category chart, monthly trend, budget table, insights, terminal simulation, passing tests. Never commit personal financial data.
