# Data dictionary

- transaction_id: unique transaction identifier (string)
- date: transaction date, ISO YYYY-MM-DD
- category: one of ten supported spending categories
- description: nonempty free-text purpose
- amount: positive expense in INR
- payment_method: UPI, Cash, Debit Card, Credit Card, Net Banking
- source: synthetic or manual
- year_month: engineered monthly aggregation key
- is_weekend: engineered Boolean derived from date
- expense_level: Low (<500), Medium (500–1999.99), High (>=2000)
