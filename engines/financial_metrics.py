import pandas as pd


def calculate_basic_metrics(sales_df, expenses_df, invoices_df):
    total_sales = sales_df["Amount"].sum() if not sales_df.empty else 0
    total_expenses = expenses_df["Amount"].sum() if not expenses_df.empty else 0

    net_profit = total_sales - total_expenses
    profit_margin = (net_profit / total_sales * 100) if total_sales > 0 else 0
    expense_ratio = (total_expenses / total_sales) if total_sales > 0 else 0

    total_invoices = len(invoices_df)
    overdue_count = (
        invoices_df[invoices_df["Status"] == "Overdue"].shape[0]
        if not invoices_df.empty else 0
    )
    overdue_ratio = overdue_count / total_invoices if total_invoices > 0 else 0

    return {
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profit_margin": profit_margin,
        "expense_ratio": expense_ratio,
        "overdue_count": overdue_count,
        "overdue_ratio": overdue_ratio
    }
def calculate_average_invoice(invoices_df):
    if invoices_df.empty:
        return 0

    return round(invoices_df["Amount"].mean(), 2)


def calculate_monthly_sales(sales_df):
    if sales_df.empty:
        return 0

    df = sales_df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    monthly = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
    )

    return round(monthly.mean(), 2)


def calculate_monthly_growth(sales_df):
    if sales_df.empty:
        return 0

    df = sales_df.copy()

    df["Date"] = pd.to_datetime(df["Date"])

    monthly = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
    )

    if len(monthly) < 2:
        return 0

    growth = monthly.pct_change().dropna()

    return round(growth.mean() * 100, 2)