import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

OUTPUT_FILE = "templates/sample_company_data.xlsx"

random.seed(42)
np.random.seed(42)

start_date = datetime(2026, 1, 1)
days = 180

customers = [
    "Al Noor Trading",
    "Riyadh Tech Store",
    "Eastern Supplies",
    "Smart Office Co",
    "Dammam Retail",
    "Najd Solutions",
]

sales_categories = ["Services", "Subscriptions", "Hardware", "Consulting"]
expense_categories = ["Salaries", "Rent", "Marketing", "Utilities", "Inventory", "Software"]

sales = []
expenses = []
invoices = []

for i in range(days):
    current_date = start_date + timedelta(days=i)

    daily_sales_count = np.random.poisson(4)

    for _ in range(daily_sales_count):
        amount = round(max(500, np.random.normal(3500, 1200)), 2)
        customer = random.choice(customers)

        sales.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Customer": customer,
            "Category": random.choice(sales_categories),
            "Amount": amount,
            "Payment Method": random.choice(["Cash", "Card", "Bank Transfer", "Online"])
        })

        if random.random() < 0.45:
            status = random.choices(["Paid", "Pending", "Overdue"], weights=[0.7, 0.2, 0.1])[0]
            issue_date = current_date
            due_date = issue_date + timedelta(days=random.choice([15, 30, 45]))

            invoices.append({
                "Customer": customer,
                "Issue Date": issue_date.strftime("%Y-%m-%d"),
                "Due Date": due_date.strftime("%Y-%m-%d"),
                "Amount": amount,
                "Status": status
            })

    if current_date.day == 1:
        monthly_fixed = {
            "Salaries": 52000,
            "Rent": 18000,
            "Software": 4500
        }

        for category, amount in monthly_fixed.items():
            expenses.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": category,
                "Amount": round(np.random.normal(amount, amount * 0.05), 2),
                "Description": f"Monthly {category}"
            })

    daily_expenses_count = np.random.poisson(2)

    for _ in range(daily_expenses_count):
        category = random.choice(["Marketing", "Utilities", "Inventory"])
        base_amount = {
            "Marketing": 1200,
            "Utilities": 350,
            "Inventory": 2400
        }[category]

        amount = round(max(100, np.random.normal(base_amount, base_amount * 0.35)), 2)

        expenses.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount,
            "Description": f"Regular {category} expense"
        })

company = pd.DataFrame([{
    "Company Name": "Smart Retail SME",
    "Industry": "Retail Technology",
    "City": "Riyadh",
    "Employees": 18,
    "Start Date": "2022-01-01"
}])

employees = pd.DataFrame([
    {"Department": "Sales", "Salary": 8500, "Hire Date": "2023-01-10"},
    {"Department": "Operations", "Salary": 7500, "Hire Date": "2022-09-01"},
    {"Department": "Finance", "Salary": 9500, "Hire Date": "2023-05-15"},
    {"Department": "Marketing", "Salary": 7000, "Hire Date": "2024-02-20"},
    {"Department": "Support", "Salary": 6000, "Hire Date": "2024-04-01"},
])

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    company.to_excel(writer, sheet_name="Company", index=False)
    pd.DataFrame(sales).to_excel(writer, sheet_name="Sales", index=False)
    pd.DataFrame(expenses).to_excel(writer, sheet_name="Expenses", index=False)
    pd.DataFrame(invoices).to_excel(writer, sheet_name="Invoices", index=False)
    employees.to_excel(writer, sheet_name="Employees", index=False)

print(f"Sample company data created: {OUTPUT_FILE}")