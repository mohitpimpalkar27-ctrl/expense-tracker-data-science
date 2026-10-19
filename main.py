"""Run with: streamlit run main.py"""
from pathlib import Path
import datetime as dt
import pandas as pd
import streamlit as st
from src.data_generator import generate_synthetic_data, CATEGORIES, PAYMENT_METHODS
from src.data_cleaning import clean_expense_data
from src.expense_analysis import calculate_summary, category_analysis, monthly_analysis, payment_analysis, spending_patterns
from src.budget_analysis import budget_analysis, DEFAULT_BUDGETS
from src.insights import generate_insights
from src.database import fetch_expenses
from src.expense_manager import add_expense, edit_expense, remove_expense

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Expense Tracker Analytics", page_icon="💰", layout="wide")
st.title("💰 Expense Tracker | Financial Analytics")
st.caption("Demo data is synthetic. Manually entered records stay in a local SQLite database.")
page = st.sidebar.radio("Navigate", ["Dashboard", "Manage Expenses", "Analytics", "Budget Planner", "Insights"])
mode = st.sidebar.radio("Dataset", ["Synthetic demo", "Manual transactions", "Upload CSV"])
if mode == "Synthetic demo":
    csv_path = ROOT / "data" / "synthetic_expenses.csv"
    raw = pd.read_csv(csv_path) if csv_path.exists() else generate_synthetic_data()
elif mode == "Manual transactions":
    raw = fetch_expenses()
else:
    uploaded = st.sidebar.file_uploader("Upload expense CSV", type="csv")
    raw = pd.read_csv(uploaded) if uploaded else pd.DataFrame(columns=["transaction_id","date","category","description","amount","payment_method"])
try:
    df, rejected = clean_expense_data(raw)
except Exception as exc:
    st.error(f"Invalid input data: {exc}")
    st.stop()
if len(rejected):
    st.warning(f"{len(rejected)} invalid/duplicate rows excluded. Download and inspect them before proceeding.")
    st.sidebar.download_button("Download rejected rows", rejected.to_csv(index=False), "rejected_rows.csv")
if not df.empty:
    start = pd.to_datetime(df["date"]).min().date()
    end = pd.to_datetime(df["date"]).max().date()
    chosen = st.sidebar.date_input("Date range", value=(start, end), min_value=start, max_value=end)
    if isinstance(chosen, tuple) and len(chosen) == 2:
        df = df.loc[(pd.to_datetime(df["date"]).dt.date >= chosen[0]) & (pd.to_datetime(df["date"]).dt.date <= chosen[1])]
    selected = st.sidebar.multiselect("Categories", CATEGORIES, default=CATEGORIES)
    df = df[df["category"].isin(selected)]

if page == "Manage Expenses":
    st.subheader("Add a manual transaction")
    with st.form("new_expense"):
        date = st.date_input("Date", dt.date.today())
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description")
        amount = st.number_input("Amount (INR)", min_value=0.01, value=100.0, step=10.0)
        method = st.selectbox("Payment method", PAYMENT_METHODS)
        submitted = st.form_submit_button("Save transaction")
        if submitted:
            try:
                tid = add_expense(date, category, description, amount, method)
                st.success(f"Saved {tid}. Switch dataset to 'Manual transactions' to analyze it.")
            except Exception as exc:
                st.error(str(exc))
    manual = fetch_expenses()
    st.subheader("Saved manual transactions")
    st.dataframe(manual, use_container_width=True)
    if not manual.empty:
        ids = manual["transaction_id"].tolist()
        with st.expander("Edit transaction"):
            selected_id = st.selectbox("Transaction ID", ids, key="edit_id")
            old = manual.set_index("transaction_id").loc[selected_id]
            with st.form("edit_form"):
                edate = st.date_input("New date", pd.Timestamp(old["date"]).date())
                ecat = st.selectbox("New category", CATEGORIES, index=CATEGORIES.index(old["category"]))
                edesc = st.text_input("New description", old["description"])
                eamount = st.number_input("New amount", min_value=0.01, value=float(old["amount"]))
                emethod = st.selectbox("New payment method", PAYMENT_METHODS, index=PAYMENT_METHODS.index(old["payment_method"]))
                if st.form_submit_button("Update"):
                    try:
                        edit_expense(selected_id, edate, ecat, edesc, eamount, emethod)
                        st.success("Updated. Refresh the page to see changes.")
                    except Exception as exc:
                        st.error(str(exc))
        with st.expander("Delete transaction"):
            delete_id = st.selectbox("Select ID to delete", ids)
            if st.button("Confirm delete", type="secondary"):
                remove_expense(delete_id)
                st.success("Deleted. Refresh the page to see changes.")
    st.stop()

if df.empty:
    st.info("No transactions in the selected dataset or filters. Add records or select another dataset.")
    st.stop()
summary = calculate_summary(df)
months = sorted(pd.to_datetime(df["date"]).dt.strftime("%Y-%m").unique())

if page == "Dashboard":
    st.subheader("Financial Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total expenses", f"₹{summary['total_expenses']:,.2f}")
    c2.metric("Transactions", f"{summary['transaction_count']:,}")
    c3.metric("Average transaction", f"₹{summary['average_transaction']:,.2f}")
    c4.metric("Top category", summary["highest_category"])
    st.subheader("Monthly expenses")
    st.line_chart(monthly_analysis(df).set_index("year_month")["total_amount"])
    st.subheader("Category expenses")
    st.bar_chart(category_analysis(df).set_index("category")["total_amount"])
    st.dataframe(df, use_container_width=True)
    st.download_button("Download filtered transactions", df.to_csv(index=False), "filtered_expenses.csv")
elif page == "Analytics":
    st.subheader("Category analysis")
    st.dataframe(category_analysis(df), use_container_width=True)
    st.bar_chart(category_analysis(df).set_index("category")["total_amount"])
    st.subheader("Monthly trend and MoM growth")
    st.dataframe(monthly_analysis(df), use_container_width=True)
    st.line_chart(monthly_analysis(df).set_index("year_month")["total_amount"])
    st.subheader("Payment methods")
    st.dataframe(payment_analysis(df), use_container_width=True)
    st.subheader("Weekday vs weekend")
    st.dataframe(spending_patterns(df), use_container_width=True)
elif page == "Budget Planner":
    month = st.selectbox("Budget month", months)
    st.caption("Budget values apply to one month, not the entire selected date range.")
    budgets = {}
    with st.expander("Edit category budgets", expanded=True):
        for cat in CATEGORIES:
            budgets[cat] = st.number_input(cat, min_value=0.0, value=float(DEFAULT_BUDGETS[cat]), step=500.0)
    report = budget_analysis(df, budgets, month)
    st.dataframe(report, use_container_width=True)
    st.bar_chart(report.set_index("category")[["budget", "actual"]])
    st.download_button("Download budget report", report.to_csv(index=False), f"budget_{month}.csv")
else:
    month = st.selectbox("Month for budget alerts", months)
    for note in generate_insights(df, month=month):
        st.info(note)
