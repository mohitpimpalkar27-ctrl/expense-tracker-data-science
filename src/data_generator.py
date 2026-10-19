"""Reproducible, explicitly synthetic 2025 expense transactions."""
from pathlib import Path
import numpy as np
import pandas as pd

CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Education", "Healthcare", "Rent", "Utilities", "Travel", "Others"]
PAYMENT_METHODS = ["UPI", "Cash", "Debit Card", "Credit Card", "Net Banking"]
BASE = {"Food": 260, "Transport": 110, "Shopping": 850, "Entertainment": 420, "Education": 700,
        "Healthcare": 500, "Rent": 9000, "Utilities": 1200, "Travel": 1800, "Others": 350}
DESCRIPTIONS = {"Food": "Meals / groceries", "Transport": "Commute", "Shopping": "Retail purchase",
                "Entertainment": "Movie / subscription", "Education": "Learning material", "Healthcare": "Medical purchase",
                "Rent": "Monthly rent", "Utilities": "Electricity / internet", "Travel": "Trip expense", "Others": "Miscellaneous"}

def generate_synthetic_data(n=2000, seed=42):
    """Return n synthetic records; includes 12 monthly rent payments when n>=12."""
    if n < 12:
        raise ValueError("n must be >= 12 to include monthly rent")
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    rent_dates = pd.to_datetime([f"2025-{m:02d}-01" for m in range(1, 13)])
    sampled_dates = rng.choice(dates.to_numpy(), size=n - 12, replace=True)
    sampled_categories = rng.choice([c for c in CATEGORIES if c != "Rent"], size=n - 12,
        p=np.array([.32, .18, .13, .10, .07, .05, .07, .03, .04]) / .99)
    rows = []
    for date, category in zip(sampled_dates, sampled_categories):
        dt = pd.Timestamp(date)
        seasonal = 1.18 if dt.month in (10, 11, 12) else 1.0
        amount = round(float(rng.lognormal(np.log(BASE[category]), .45) * seasonal), 2)
        rows.append((dt, category, DESCRIPTIONS[category], amount, rng.choice(PAYMENT_METHODS, p=[.55,.15,.14,.12,.04])))
    for dt in rent_dates:
        rows.append((dt, "Rent", "Monthly rent", 9000.0, "Net Banking"))
    frame = pd.DataFrame(rows, columns=["date", "category", "description", "amount", "payment_method"])
    frame = frame.sort_values("date").reset_index(drop=True)
    frame.insert(0, "transaction_id", [f"EXP{i:05d}" for i in range(1, len(frame) + 1)])
    frame["date"] = frame["date"].dt.strftime("%Y-%m-%d")
    frame["source"] = "synthetic"
    return frame

if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "data" / "synthetic_expenses.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_synthetic_data().to_csv(output, index=False)
    print(f"Created {output}")
