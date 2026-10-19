"""Budget-vs-actual comparison with safe zero-budget handling."""
import pandas as pd

DEFAULT_BUDGETS = {"Food": 16000, "Transport": 5500, "Shopping": 15000, "Entertainment": 6500,
                   "Education": 8000, "Healthcare": 6000, "Rent": 9000, "Utilities": 6000,
                   "Travel": 9000, "Others": 7000}

def budget_analysis(df, budgets=None, month=None):
    """Budget values are MONTHLY per category; month is YYYY-MM."""
    budgets = DEFAULT_BUDGETS if budgets is None else budgets
    d = df.copy()
    if month is not None:
        d = d.loc[pd.to_datetime(d["date"]).dt.strftime("%Y-%m") == month]
    actual = d.groupby("category")["amount"].sum()
    categories = sorted(set(budgets) | set(actual.index))
    rows = []
    for cat in categories:
        planned = float(budgets.get(cat, 0))
        if planned < 0:
            raise ValueError("Budgets cannot be negative")
        spent = float(actual.get(cat, 0))
        utilization = round(spent / planned * 100, 2) if planned > 0 else None
        status = "Over Budget" if spent > planned else "Within Budget"
        rows.append({"category": cat, "budget": planned, "actual": round(spent, 2),
                     "variance": round(planned - spent, 2), "utilization_pct": utilization, "status": status})
    return pd.DataFrame(rows)
