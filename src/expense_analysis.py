"""Financial summaries and spending patterns."""
import pandas as pd

def calculate_summary(df):
    total = float(df["amount"].sum())
    category = category_analysis(df)
    return {"total_expenses": round(total, 2), "transaction_count": int(len(df)),
            "average_transaction": round(total / len(df), 2) if len(df) else 0.0,
            "highest_category": category.iloc[0]["category"] if len(category) else "N/A"}

def category_analysis(df):
    return (df.groupby("category", as_index=False)["amount"].sum()
            .rename(columns={"amount": "total_amount"}).sort_values("total_amount", ascending=False).reset_index(drop=True))

def monthly_analysis(df):
    if df.empty:
        return pd.DataFrame(columns=["year_month", "total_amount", "mom_change_pct"])
    d = df.copy()
    d["year_month"] = pd.to_datetime(d["date"]).dt.to_period("M")
    grouped = d.groupby("year_month")["amount"].sum().sort_index()
    # Fill missing months inside the observed date range with zero spending.
    full = pd.period_range(grouped.index.min(), grouped.index.max(), freq="M")
    grouped = grouped.reindex(full, fill_value=0)
    previous = grouped.shift(1)
    change = ((grouped - previous) / previous * 100).where(previous > 0)
    return pd.DataFrame({"year_month": grouped.index.astype(str), "total_amount": grouped.values,
                         "mom_change_pct": change.values})

def payment_analysis(df):
    return (df.groupby("payment_method", as_index=False)
            .agg(transaction_count=("amount", "size"), total_amount=("amount", "sum"))
            .sort_values("transaction_count", ascending=False).reset_index(drop=True))

def spending_patterns(df):
    if df.empty:
        return pd.DataFrame(columns=["day_type", "total_amount", "transaction_count"])
    d = df.copy()
    dates = pd.to_datetime(d["date"])
    d["day_type"] = dates.dt.dayofweek.map(lambda n: "Weekend" if n >= 5 else "Weekday")
    return d.groupby("day_type", as_index=False).agg(total_amount=("amount", "sum"), transaction_count=("amount", "size"))
