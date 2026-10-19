import pandas as pd
from src.data_generator import generate_synthetic_data
from src.data_cleaning import clean_expense_data
from src.expense_analysis import calculate_summary, monthly_analysis
from src.budget_analysis import budget_analysis

def test_synthetic_reproducible():
    assert generate_synthetic_data(100, seed=7).equals(generate_synthetic_data(100, seed=7))

def test_clean_data():
    clean, rejected = clean_expense_data(generate_synthetic_data(100))
    assert len(clean) == 100 and rejected.empty

def test_total():
    df = pd.DataFrame({"amount": [500, 300, 200], "category": ["Food"] * 3})
    assert calculate_summary(df)["total_expenses"] == 1000

def test_budget_variance():
    df = pd.DataFrame({"date": ["2025-12-01"], "category": ["Food"], "amount": [6200]})
    row = budget_analysis(df, {"Food": 5000}, "2025-12").iloc[0]
    assert row["variance"] == -1200 and row["utilization_pct"] == 124

def test_zero_previous_month():
    df = pd.DataFrame({"date": ["2025-01-01", "2025-03-01"], "amount": [100, 200]})
    result = monthly_analysis(df)
    assert pd.isna(result.iloc[2]["mom_change_pct"])
