"""Local SQLite storage for manually entered records (excluded from Git)."""
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "expenses.sqlite3"

def initialize_database(db_path=DB_PATH):
    with sqlite3.connect(db_path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS expenses (
            transaction_id TEXT PRIMARY KEY, date TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT NOT NULL, amount REAL NOT NULL CHECK(amount > 0),
            payment_method TEXT NOT NULL, source TEXT NOT NULL DEFAULT 'manual')""")

def insert_expense(record, db_path=DB_PATH):
    initialize_database(db_path)
    with sqlite3.connect(db_path) as con:
        con.execute("INSERT INTO expenses VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (record["transaction_id"], record["date"], record["category"],
                     record["description"], record["amount"], record["payment_method"], "manual"))

def fetch_expenses(db_path=DB_PATH):
    initialize_database(db_path)
    with sqlite3.connect(db_path) as con:
        return pd.read_sql_query("SELECT * FROM expenses ORDER BY date", con)

def delete_expense(transaction_id, db_path=DB_PATH):
    initialize_database(db_path)
    with sqlite3.connect(db_path) as con:
        con.execute("DELETE FROM expenses WHERE transaction_id=?", (transaction_id,))

def update_expense(record, db_path=DB_PATH):
    initialize_database(db_path)
    with sqlite3.connect(db_path) as con:
        con.execute("""UPDATE expenses SET date=?, category=?, description=?, amount=?, payment_method=?
                       WHERE transaction_id=?""", (record["date"], record["category"], record["description"],
                        record["amount"], record["payment_method"], record["transaction_id"]))
