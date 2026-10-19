"""Generate synthetic CSVs, analytical reports and PNGs without the web dashboard."""
from pathlib import Path
import pandas as pd
from src.data_generator import generate_synthetic_data
from src.data_cleaning import clean_expense_data
from src.feature_engineering import add_features
from src.expense_analysis import calculate_summary, category_analysis, monthly_analysis, payment_analysis, spending_patterns
from src.budget_analysis import budget_analysis
from src.insights import generate_insights
from src.visualization import save_charts

ROOT = Path(__file__).resolve().parent
for folder in ["data", "outputs", "images"]:
    (ROOT / folder).mkdir(exist_ok=True)
raw = generate_synthetic_data(n=2000, seed=42)
raw.to_csv(ROOT / "data/synthetic_expenses.csv", index=False)
clean, rejected = clean_expense_data(raw)
clean.to_csv(ROOT / "data/cleaned_expenses.csv", index=False)
processed = add_features(clean)
processed.to_csv(ROOT / "data/processed_expenses.csv", index=False)
summary = calculate_summary(clean)
pd.DataFrame([summary]).to_csv(ROOT / "outputs/financial_summary.csv", index=False)
category_analysis(clean).to_csv(ROOT / "outputs/category_analysis.csv", index=False)
monthly_analysis(clean).to_csv(ROOT / "outputs/monthly_analysis.csv", index=False)
payment_analysis(clean).to_csv(ROOT / "outputs/payment_analysis.csv", index=False)
spending_patterns(clean).to_csv(ROOT / "outputs/spending_patterns.csv", index=False)
budget_analysis(clean, month="2025-12").to_csv(ROOT / "outputs/budget_analysis.csv", index=False)
notes = generate_insights(clean, month="2025-12")
(ROOT / "outputs/financial_insights.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")
charts = save_charts(clean, ROOT / "images", month="2025-12")
print("SYNTHETIC EXPENSE TRACKER — SIMULATION COMPLETE")
print(f"Transactions: {len(clean)}; rejected: {len(rejected)}")
print(f"Total expenses: ₹{summary['total_expenses']:,.2f}")
print(f"Highest category: {summary['highest_category']}")
print("Insights:")
for note in notes:
    print(" -", note)
print("Charts saved:")
for chart in charts:
    print(" -", chart)
