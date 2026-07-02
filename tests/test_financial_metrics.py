import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engines.financial_metrics import (
    calculate_basic_metrics,
    calculate_average_invoice,
    calculate_monthly_sales,
    calculate_monthly_growth,
)

from engines.financial_score import calculate_financial_health


sales = pd.read_excel("templates/sample_company_data.xlsx", sheet_name="Sales")
expenses = pd.read_excel("templates/sample_company_data.xlsx", sheet_name="Expenses")
invoices = pd.read_excel("templates/sample_company_data.xlsx", sheet_name="Invoices")


metrics = calculate_basic_metrics(sales, expenses, invoices)

health = calculate_financial_health(
    metrics["profit_margin"],
    metrics["expense_ratio"],
    metrics["overdue_ratio"]
)


print("Basic Metrics")
print("--------------------")
print(metrics)

print("\nFinancial Health")
print("--------------------")
print(health)

print("\nExtra Metrics")
print("--------------------")
print("Average Invoice:", calculate_average_invoice(invoices))
print("Average Monthly Sales:", calculate_monthly_sales(sales))
print("Monthly Growth:", calculate_monthly_growth(sales))