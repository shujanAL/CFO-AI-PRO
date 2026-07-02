import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from engines.financial_engine import (
    calculate_financial_health,
    detect_expense_anomalies,
    generate_recommendations,
    generate_ai_summary
)
DB_NAME = "cfo_ai.db"

st.set_page_config(page_title="CFO AI Pro", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_NAME)
    sales = pd.read_sql_query("SELECT * FROM sales", conn)
    expenses = pd.read_sql_query("SELECT * FROM expenses", conn)
    invoices = pd.read_sql_query("SELECT * FROM invoices", conn)
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()

    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    expenses["expense_date"] = pd.to_datetime(expenses["expense_date"])
    invoices["issue_date"] = pd.to_datetime(invoices["issue_date"])
    invoices["due_date"] = pd.to_datetime(invoices["due_date"])

    return sales, expenses, invoices, customers


sales, expenses, invoices, customers = load_data()

st.title("CFO AI Pro")
st.caption("AI-powered financial intelligence platform for SMEs")

min_date = min(sales["sale_date"].min(), expenses["expense_date"].min())
max_date = max(sales["sale_date"].max(), expenses["expense_date"].max())

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = min_date
    end_date = max_date

sales_f = sales[(sales["sale_date"] >= start_date) & (sales["sale_date"] <= end_date)]
expenses_f = expenses[(expenses["expense_date"] >= start_date) & (expenses["expense_date"] <= end_date)]
invoices_f = invoices[(invoices["issue_date"] >= start_date) & (invoices["issue_date"] <= end_date)]

total_sales = sales_f["amount"].sum()
total_expenses = expenses_f["amount"].sum()
net_profit = total_sales - total_expenses
profit_margin = (net_profit / total_sales * 100) if total_sales > 0 else 0
overdue_count = invoices_f[invoices_f["status"] == "Overdue"].shape[0]
overdue_ratio = overdue_count / len(invoices_f) if len(invoices_f) > 0 else 0

top_expense_category = (
    expenses_f.groupby("category")["amount"].sum().idxmax()
    if not expenses_f.empty else None
)

health_score, health_status = calculate_financial_health(
    total_sales,
    total_expenses,
    net_profit,
    profit_margin,
    overdue_ratio
)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"{total_sales:,.0f} SAR")
col2.metric("Total Expenses", f"{total_expenses:,.0f} SAR")
col3.metric("Net Profit", f"{net_profit:,.0f} SAR")
col4.metric("Profit Margin", f"{profit_margin:.1f}%")
st.subheader("Financial Health Score")

score_col, status_col, alert_col = st.columns(3)

score_col.metric("Health Score", f"{health_score}/100")
status_col.metric("Status", health_status)
alert_col.metric("Overdue Invoices", overdue_count)

if health_status == "Critical":
    st.error("High financial risk detected. Immediate action is recommended.")
elif health_status == "Warning":
    st.warning("Financial performance needs attention.")
else:
    st.success("Financial position is stable.")
st.divider()

monthly_sales = sales_f.groupby(pd.Grouper(key="sale_date", freq="ME"))["amount"].sum().reset_index()

monthly_expenses = expenses_f.groupby(pd.Grouper(key="expense_date", freq="ME"))["amount"].sum().reset_index()
monthly = pd.merge(
    monthly_sales,
    monthly_expenses,
    left_on="sale_date",
    right_on="expense_date",
    how="outer"
).fillna(0)

monthly["month"] = monthly["sale_date"].fillna(monthly["expense_date"])
monthly["cash_flow"] = monthly["amount_x"] - monthly["amount_y"]
monthly = monthly.rename(columns={"amount_x": "Sales", "amount_y": "Expenses"})

st.subheader("Financial Performance Over Time")
fig = px.line(monthly, x="month", y=["Sales", "Expenses", "cash_flow"])
st.plotly_chart(fig, use_container_width=True)

colA, colB = st.columns(2)

with colA:
    st.subheader("Sales by Product Category")
    sales_cat = sales_f.groupby("product_category")["amount"].sum().reset_index()
    fig2 = px.bar(sales_cat, x="product_category", y="amount")
    st.plotly_chart(fig2, use_container_width=True)

with colB:
    st.subheader("Expenses by Category")
    expense_cat = expenses_f.groupby("category")["amount"].sum().reset_index()
    fig3 = px.pie(expense_cat, names="category", values="amount")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Invoice Status")
invoice_status = invoices_f["status"].value_counts().reset_index()
invoice_status.columns = ["Status", "Count"]
fig4 = px.bar(invoice_status, x="Status", y="Count")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Smart Alerts")

anomalies = detect_expense_anomalies(expenses_f)

if not anomalies.empty:
    st.warning("Unusual expenses detected.")
    st.dataframe(anomalies, use_container_width=True)
else:
    st.success("No unusual expenses detected.")

st.subheader("AI CFO Recommendations")

recommendations = generate_recommendations(
    total_sales,
    total_expenses,
    net_profit,
    profit_margin,
    overdue_count,
    top_expense_category
)

for i, rec in enumerate(recommendations, start=1):
    st.write(f"{i}. {rec}")

st.subheader("AI Financial Summary")

summary = generate_ai_summary(
    total_sales,
    total_expenses,
    net_profit,
    profit_margin,
    health_score,
    health_status
)

st.info(summary)