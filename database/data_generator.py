import sqlite3
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


DB_NAME = "cfo_ai.db"
START_DATE = datetime(2024, 1, 1)
DAYS = 730


random.seed(42)
np.random.seed(42)


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS sales;
    DROP TABLE IF EXISTS expenses;
    DROP TABLE IF EXISTS invoices;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS suppliers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT,
        city TEXT,
        customer_type TEXT,
        join_date TEXT
    );

    CREATE TABLE suppliers (
        supplier_id INTEGER PRIMARY KEY,
        supplier_name TEXT,
        category TEXT
    );

    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        sale_date TEXT,
        product_category TEXT,
        amount REAL,
        payment_method TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE expenses (
        expense_id INTEGER PRIMARY KEY,
        supplier_id INTEGER,
        expense_date TEXT,
        category TEXT,
        amount REAL,
        description TEXT,
        FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)
    );

    CREATE TABLE invoices (
        invoice_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        issue_date TEXT,
        due_date TEXT,
        amount REAL,
        status TEXT,
        paid_date TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );
    """)

    conn.commit()


def generate_customers(conn):
    cities = ["Riyadh", "Jeddah", "Dammam", "Khobar", "Madinah", "Qassim"]
    types = ["Retail", "Corporate", "Online"]

    customers = []
    for i in range(1, 151):
        customers.append({
            "customer_id": i,
            "customer_name": f"Customer_{i}",
            "city": random.choice(cities),
            "customer_type": random.choice(types),
            "join_date": (START_DATE - timedelta(days=random.randint(1, 600))).strftime("%Y-%m-%d")
        })

    pd.DataFrame(customers).to_sql("customers", conn, if_exists="append", index=False)


def generate_suppliers(conn):
    categories = ["Inventory", "Marketing", "Rent", "Utilities", "Logistics", "Software", "Salaries"]

    suppliers = []
    for i in range(1, 31):
        suppliers.append({
            "supplier_id": i,
            "supplier_name": f"Supplier_{i}",
            "category": random.choice(categories)
        })

    pd.DataFrame(suppliers).to_sql("suppliers", conn, if_exists="append", index=False)


def generate_sales(conn):
    product_categories = ["Electronics", "Accessories", "Subscriptions", "Services"]
    payment_methods = ["Card", "Bank Transfer", "Cash", "Online"]

    sales = []
    sale_id = 1

    for day in range(DAYS):
        current_date = START_DATE + timedelta(days=day)

        # Seasonality: sales increase near Ramadan/Eid and end of year
        month_factor = 1.0
        if current_date.month in [3, 4, 12]:
            month_factor = 1.35
        elif current_date.month in [7, 8]:
            month_factor = 0.85

        daily_transactions = int(np.random.poisson(9 * month_factor))

        for _ in range(daily_transactions):
            category = random.choice(product_categories)
            base_amount = {
                "Electronics": 950,
                "Accessories": 180,
                "Subscriptions": 350,
                "Services": 600
            }[category]

            amount = max(50, np.random.normal(base_amount * month_factor, base_amount * 0.35))

            sales.append({
                "sale_id": sale_id,
                "customer_id": random.randint(1, 150),
                "sale_date": current_date.strftime("%Y-%m-%d"),
                "product_category": category,
                "amount": round(amount, 2),
                "payment_method": random.choice(payment_methods)
            })
            sale_id += 1

    pd.DataFrame(sales).to_sql("sales", conn, if_exists="append", index=False)


def generate_expenses(conn):
    categories = ["Inventory", "Marketing", "Rent", "Utilities", "Logistics", "Software", "Salaries"]
    expenses = []
    expense_id = 1

    for day in range(DAYS):
        current_date = START_DATE + timedelta(days=day)

        # Monthly fixed costs
        if current_date.day == 1:
            fixed_costs = {
                "Rent": 18000,
                "Salaries": 52000,
                "Software": 4500
            }

            for category, amount in fixed_costs.items():
                expenses.append({
                    "expense_id": expense_id,
                    "supplier_id": random.randint(1, 30),
                    "expense_date": current_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": round(np.random.normal(amount, amount * 0.05), 2),
                    "description": f"Monthly {category}"
                })
                expense_id += 1

        # Daily variable costs
        daily_expenses = np.random.poisson(3)

        for _ in range(daily_expenses):
            category = random.choice(["Inventory", "Marketing", "Utilities", "Logistics"])
            base_amount = {
                "Inventory": 2500,
                "Marketing": 900,
                "Utilities": 350,
                "Logistics": 700
            }[category]

            amount = max(50, np.random.normal(base_amount, base_amount * 0.45))

            # Inject anomalies
            if random.random() < 0.015:
                amount *= random.randint(3, 6)
                description = f"Unusual high {category} expense"
            else:
                description = f"Regular {category} expense"

            expenses.append({
                "expense_id": expense_id,
                "supplier_id": random.randint(1, 30),
                "expense_date": current_date.strftime("%Y-%m-%d"),
                "category": category,
                "amount": round(amount, 2),
                "description": description
            })
            expense_id += 1

    pd.DataFrame(expenses).to_sql("expenses", conn, if_exists="append", index=False)


def generate_invoices(conn):
    sales_df = pd.read_sql_query("SELECT sale_id, customer_id, sale_date, amount FROM sales", conn)

    invoices = []
    invoice_id = 1

    sampled_sales = sales_df.sample(frac=0.45, random_state=42)

    for _, row in sampled_sales.iterrows():
        issue_date = datetime.strptime(row["sale_date"], "%Y-%m-%d")
        due_date = issue_date + timedelta(days=random.choice([15, 30, 45]))

        status = random.choices(
            ["Paid", "Pending", "Overdue"],
            weights=[0.72, 0.18, 0.10]
        )[0]

        paid_date = None
        if status == "Paid":
            paid_date = issue_date + timedelta(days=random.randint(1, 35))

        invoices.append({
            "invoice_id": invoice_id,
            "customer_id": int(row["customer_id"]),
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "amount": round(float(row["amount"]), 2),
            "status": status,
            "paid_date": paid_date.strftime("%Y-%m-%d") if paid_date else None
        })
        invoice_id += 1

    pd.DataFrame(invoices).to_sql("invoices", conn, if_exists="append", index=False)


def main():
    conn = connect_db()
    create_tables(conn)

    generate_customers(conn)
    generate_suppliers(conn)
    generate_sales(conn)
    generate_expenses(conn)
    generate_invoices(conn)

    conn.close()

    print("CFO AI database generated successfully.")
    print(f"Database file: {DB_NAME}")


if __name__ == "__main__":
    main()