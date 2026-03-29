from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from datetime import datetime

# Create Flask app
app = Flask(__name__)
app.secret_key = "budget_tracker_secret_key"

# Database and allowed values
DB_NAME = "budget.db"
ALLOWED_TYPES = ["income", "expense"]
ALLOWED_CATEGORIES = [
    "Salary", "Food", "Transport", "Shopping",
    "Bills", "Entertainment", "Other"
]


# Open database connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# Create transactions table if needed
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            description TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Validate form input
def validate_transaction_form(form):
    transaction_type = form.get("type", "").strip()
    category = form.get("category", "").strip()
    amount_raw = form.get("amount", "").strip()
    description = form.get("description", "").strip()
    date_raw = form.get("date", "").strip()

    if transaction_type not in ALLOWED_TYPES:
        return None, "Invalid transaction type."

    if category not in ALLOWED_CATEGORIES:
        return None, "Invalid category."

    try:
        amount = float(amount_raw)
        if amount <= 0:
            return None, "Amount must be greater than 0."
    except ValueError:
        return None, "Amount must be a valid number."

    try:
        datetime.strptime(date_raw, "%Y-%m-%d")
    except ValueError:
        return None, "Date must be in valid YYYY-MM-DD format."

    if len(description) > 200:
        return None, "Description must be 200 characters or fewer."

    validated_data = {
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "description": description,
        "date": date_raw
    }

    return validated_data, None


# Home page
@app.route("/")
def index():
    conn = get_db_connection()

    # Get all transactions
    transactions = conn.execute("""
        SELECT * FROM transactions
        ORDER BY date DESC, id DESC
    """).fetchall()

    # Get totals
    total_income = conn.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income'
    """).fetchone()[0]

    total_expenses = conn.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense'
    """).fetchone()[0]

    # Get expense totals for pie chart
    expense_rows = conn.execute("""
        SELECT category, COALESCE(SUM(amount), 0) AS total
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    balance = total_income - total_expenses
    today = datetime.today().strftime("%Y-%m-%d")

    expense_labels = [row["category"] for row in expense_rows]
    expense_values = [row["total"] for row in expense_rows]

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        today=today,
        categories=ALLOWED_CATEGORIES,
        expense_labels=expense_labels,
        expense_values=expense_values
    )


# Add a new transaction
@app.route("/add", methods=["POST"])
def add_transaction():
    validated_data, error = validate_transaction_form(request.form)

    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO transactions (type, category, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        validated_data["type"],
        validated_data["category"],
        validated_data["amount"],
        validated_data["description"],
        validated_data["date"]
    ))
    conn.commit()
    conn.close()

    flash("Transaction added successfully.", "success")
    return redirect(url_for("index"))


# Show edit page
@app.route("/edit/<int:transaction_id>")
def edit_transaction_page(transaction_id):
    conn = get_db_connection()
    transaction = conn.execute("""
        SELECT * FROM transactions
        WHERE id = ?
    """, (transaction_id,)).fetchone()
    conn.close()

    if transaction is None:
        flash("Transaction not found.", "error")
        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        transaction=transaction,
        categories=ALLOWED_CATEGORIES
    )


# Update an existing transaction
@app.route("/update/<int:transaction_id>", methods=["POST"])
def update_transaction(transaction_id):
    validated_data, error = validate_transaction_form(request.form)

    if error:
        flash(error, "error")
        return redirect(url_for("edit_transaction_page", transaction_id=transaction_id))

    conn = get_db_connection()
    existing = conn.execute("""
        SELECT id FROM transactions
        WHERE id = ?
    """, (transaction_id,)).fetchone()

    if existing is None:
        conn.close()
        flash("Transaction not found.", "error")
        return redirect(url_for("index"))

    conn.execute("""
        UPDATE transactions
        SET type = ?, category = ?, amount = ?, description = ?, date = ?
        WHERE id = ?
    """, (
        validated_data["type"],
        validated_data["category"],
        validated_data["amount"],
        validated_data["description"],
        validated_data["date"],
        transaction_id
    ))
    conn.commit()
    conn.close()

    flash("Transaction updated successfully.", "success")
    return redirect(url_for("index"))


# Delete a transaction
@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    conn = get_db_connection()
    existing = conn.execute("""
        SELECT id FROM transactions
        WHERE id = ?
    """, (transaction_id,)).fetchone()

    if existing is None:
        conn.close()
        flash("Transaction not found.", "error")
        return redirect(url_for("index"))

    conn.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (transaction_id,))
    conn.commit()
    conn.close()

    flash("Transaction deleted successfully.", "success")
    return redirect(url_for("index"))


# Run the app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)