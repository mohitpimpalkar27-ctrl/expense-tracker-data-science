"""Save reproducible matplotlib visualizations."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .expense_analysis import category_analysis, monthly_analysis, payment_analysis
from .budget_analysis import budget_analysis

def save_charts(df, output_dir, month=None, budgets=None):
    dest = Path(output_dir)
    dest.mkdir(parents=True, exist_ok=True)
    paths = []
    def save(fig, name):
        fig.tight_layout()
        path = dest / name
        fig.savefig(path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        paths.append(str(path))
    cat = category_analysis(df)
    if not cat.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(cat["category"], cat["total_amount"])
        ax.set_title("Expense by Category")
        ax.set_ylabel("Amount (INR)")
        ax.tick_params(axis="x", rotation=40)
        save(fig, "category_analysis.png")
    mon = monthly_analysis(df)
    if not mon.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(mon["year_month"], mon["total_amount"], marker="o")
        ax.set_title("Monthly Expense Trend")
        ax.set_ylabel("Amount (INR)")
        ax.tick_params(axis="x", rotation=40)
        save(fig, "monthly_trends.png")
    pay = payment_analysis(df)
    if not pay.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.pie(pay["transaction_count"], labels=pay["payment_method"], autopct="%1.1f%%")
        ax.set_title("Payment Methods by Transaction Count")
        save(fig, "payment_analysis.png")
    if month is not None:
        b = budget_analysis(df, budgets, month)
        fig, ax = plt.subplots(figsize=(11, 5))
        x = list(range(len(b)))
        ax.bar([i - .2 for i in x], b["budget"], width=.4, label="Budget")
        ax.bar([i + .2 for i in x], b["actual"], width=.4, label="Actual")
        ax.set_xticks(x, b["category"], rotation=40)
        ax.set_ylabel("Amount (INR)")
        ax.set_title(f"Budget vs Actual: {month}")
        ax.legend()
        save(fig, "budget_analysis.png")
    return paths
