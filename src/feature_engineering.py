"""Time features and documented spending bands."""
import numpy as np
import pandas as pd

def add_features(df):
    out = df.copy()
    dates = pd.to_datetime(out["date"])
    out["year"] = dates.dt.year
    out["month"] = dates.dt.month
    out["month_name"] = dates.dt.month_name()
    out["year_month"] = dates.dt.to_period("M").astype(str)
    out["day_of_week"] = dates.dt.day_name()
    out["quarter"] = "Q" + dates.dt.quarter.astype(str)
    out["is_weekend"] = dates.dt.dayofweek >= 5
    out["expense_level"] = np.select([out["amount"] < 500, out["amount"] < 2000], ["Low", "Medium"], default="High")
    return out
