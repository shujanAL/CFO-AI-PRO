from engines.financial_score import calculate_financial_health
import pandas as pd

def simulate_decision(
    metrics,
    scenario_type,
    action,
    category=None,
    percentage=0,
    salary=0,
    employee_count=1
):
    new_sales = metrics["total_sales"]
    new_expenses = metrics["total_expenses"]

    if scenario_type == "Revenue":
        if action == "Increase Sales":
            new_sales = new_sales * (1 + percentage / 100)
        elif action == "Decrease Sales":
            new_sales = new_sales * (1 - percentage / 100)

    elif scenario_type == "Expenses":
        if action == "Increase Expense":
            new_expenses = new_expenses * (1 + percentage / 100)
        elif action == "Reduce Expense":
            new_expenses = new_expenses * (1 - percentage / 100)

    elif scenario_type == "Employees":
        annual_cost = salary * employee_count * 12

        if action == "Hire Employee":
            new_expenses = new_expenses + annual_cost
        elif action == "Lay Off Employee":
            new_expenses = max(0, new_expenses - annual_cost)

    new_profit = new_sales - new_expenses
    new_profit_margin = (new_profit / new_sales * 100) if new_sales > 0 else 0
    new_expense_ratio = (new_expenses / new_sales) if new_sales > 0 else 0

    new_health = calculate_financial_health(
        new_profit_margin,
        new_expense_ratio,
        metrics["overdue_ratio"]
    )

    return {
        "new_sales": new_sales,
        "new_expenses": new_expenses,
        "new_profit": new_profit,
        "new_profit_margin": new_profit_margin,
        "new_health_score": new_health["score"],
        "new_health_status": new_health["status"]
    }

def update_expense_category(expenses_df, category, action, percentage):

    df = expenses_df.copy()

    mask = df["Category"] == category

    if action == "Increase Expense":
        df.loc[mask, "Amount"] *= (1 + percentage / 100)

    elif action == "Reduce Expense":
        df.loc[mask, "Amount"] *= (1 - percentage / 100)

    return df