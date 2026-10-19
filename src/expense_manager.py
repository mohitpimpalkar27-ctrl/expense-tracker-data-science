"""Validation layer for CRUD operations."""
import uuid
import pandas as pd
from .data_generator import CATEGORIES, PAYMENT_METHODS
from .database import insert_expense, update_expense, delete_expense

def validate_record(date, category, description, amount, payment_method):
    date = pd.Timestamp(date).strftime("%Y-%m-%d")
    if category not in CATEGORIES or payment_method not in PAYMENT_METHODS:
        raise ValueError("Unsupported category or payment method")
    if not description.strip() or float(amount) <= 0:
        raise ValueError("Description must be nonempty and amount positive")
    return {"date": date, "category": category, "description": description.strip(),
            "amount": round(float(amount), 2), "payment_method": payment_method}

def add_expense(date, category, description, amount, payment_method):
    record = validate_record(date, category, description, amount, payment_method)
    record["transaction_id"] = "MAN-" + uuid.uuid4().hex[:12].upper()
    insert_expense(record)
    return record["transaction_id"]

def edit_expense(transaction_id, date, category, description, amount, payment_method):
    record = validate_record(date, category, description, amount, payment_method)
    record["transaction_id"] = transaction_id
    update_expense(record)

def remove_expense(transaction_id):
    delete_expense(transaction_id)
