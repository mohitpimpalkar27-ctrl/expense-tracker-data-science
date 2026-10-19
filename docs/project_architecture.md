# Architecture

Synthetic CSV / Manual form (SQLite) / Uploaded CSV → validation → Pandas analytics → Matplotlib CLI reports or Streamlit dashboard → rule-based insights and budget comparisons.

The app never mixes synthetic and manual datasets unless the user explicitly prepares a combined CSV. The local database is ignored by Git.
