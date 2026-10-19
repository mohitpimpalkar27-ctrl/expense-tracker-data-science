# Methodology

1. Generate 2,000 reproducible synthetic 2025 expenses with NumPy RNG seed 42.
2. Validate categories, methods, positive amounts, dates, and transaction IDs.
3. Derive year/month/quarter/weekend and spending-level features.
4. Aggregate by category, month, and payment method using Pandas.
5. Compare December 2025 spending to illustrative per-category monthly budgets.
6. Produce Matplotlib charts, CSV reports, and rule-based textual insights.
7. View and add manual expenses through the Streamlit/SQLite app.
