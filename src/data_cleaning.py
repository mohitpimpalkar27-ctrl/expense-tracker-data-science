"""Validate expense records without silently discarding questionable data."""
import pandas as pd
from .data_generator import CATEGORIES, PAYMENT_METHODS

REQUIRED = ["transaction_id", "date", "category", "description", "amount", "payment_method"]

def clean_expense_data(df):
    missing = set(REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    data = df.copy()
    data["category"] = data["category"].astype("string").str.strip().str.title()
    data["payment_method"] = data["payment_method"].astype("string").str.strip()
    data["description"] = data["description"].astype("string").str.strip()
    data["transaction_id"] = data["transaction_id"].astype("string").str.strip()
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    invalid = (data["date"].isna() | data["amount"].isna() | (data["amount"] <= 0)
               | ~data["category"].isin(CATEGORIES) | ~data["payment_method"].isin(PAYMENT_METHODS)
               | data["transaction_id"].isna() | (data["transaction_id"] == "")
               | data["transaction_id"].duplicated(keep=False)
               | data["description"].isna() | (data["description"] == ""))
    rejected = data.loc[invalid].copy()
    clean = data.loc[~invalid].copy().sort_values("date").reset_index(drop=True)
    clean["date"] = clean["date"].dt.strftime("%Y-%m-%d")
    return clean, rejected
