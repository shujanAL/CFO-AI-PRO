import sqlite3
import pandas as pd


def build_database_from_excel(excel_path, db_path="database/cfo_ai_uploaded.db"):
    conn = sqlite3.connect(db_path)

    company = pd.read_excel(excel_path, sheet_name="Company")
    sales = pd.read_excel(excel_path, sheet_name="Sales")
    expenses = pd.read_excel(excel_path, sheet_name="Expenses")
    invoices = pd.read_excel(excel_path, sheet_name="Invoices")
    employees = pd.read_excel(excel_path, sheet_name="Employees")

    company.to_sql("company", conn, if_exists="replace", index=False)
    sales.to_sql("sales", conn, if_exists="replace", index=False)
    expenses.to_sql("expenses", conn, if_exists="replace", index=False)
    invoices.to_sql("invoices", conn, if_exists="replace", index=False)
    employees.to_sql("employees", conn, if_exists="replace", index=False)

    conn.close()

    return db_path