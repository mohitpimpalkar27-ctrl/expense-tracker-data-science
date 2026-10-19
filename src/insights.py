"""Transparent rule-based insights, not machine-learning predictions."""
from .expense_analysis import category_analysis, monthly_analysis
from .budget_analysis import budget_analysis

def generate_insights(df, budgets=None, month=None):
    if df.empty:
        return ["No transactions are available for the selected period."]
    notes = []
    cats = category_analysis(df)
    top = cats.iloc[0]
    share = 100 * float(top["total_amount"]) / float(df["amount"].sum())
    notes.append(f"{top['category']} is the largest expense category ({share:.1f}% of spending).")
    monthly = monthly_analysis(df)
    if len(monthly) >= 2:
        last = monthly.iloc[-1]
        if last["mom_change_pct"] == last["mom_change_pct"]:
            notes.append(f"Spending changed by {last['mom_change_pct']:+.1f}% in {last['year_month']} compared with the previous month.")
    if month is not None:
        b = budget_analysis(df, budgets, month)
        exceeded = b[b["status"] == "Over Budget"]
        for _, row in exceeded.iterrows():
            notes.append(f"{row['category']} exceeded its {month} budget by ₹{abs(row['variance']):,.2f}.")
        if exceeded.empty:
            notes.append(f"No category exceeded its configured budget in {month}.")
    return notes
