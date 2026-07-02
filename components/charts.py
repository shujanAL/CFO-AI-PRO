import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.i18n import tr


def show_monthly_sales_chart(sales_df, language="en"):
    ar = language == "ar"
    df = sales_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly["Date"] = monthly["Date"].astype(str)
    fig = px.line(monthly, x="Date", y="Amount", markers=True,
                  title="اتجاه الإيرادات الشهرية" if ar else "Monthly Revenue Trend",
                  labels={"Date": "الشهر" if ar else "Date", "Amount": "المبلغ" if ar else "Amount"})
    fig.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig, use_container_width=True)


def show_expense_breakdown(expenses_df, language="en"):
    ar = language == "ar"
    category = expenses_df.groupby("Category")["Amount"].sum().reset_index()
    if ar:
        category["Category"] = category["Category"].map(lambda value: tr(value, language))
    fig = px.pie(category, names="Category", values="Amount", hole=0.45,
                 title="توزيع المصروفات" if ar else "Expense Breakdown")
    fig.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig, use_container_width=True)


def show_forecast_chart(history_df, forecast_df, language="en"):
    ar = language == "ar"
    history = history_df.copy()
    history["Date"] = pd.to_datetime(history["Date"])
    monthly = history.groupby(history["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly["Date"] = monthly["Date"].dt.to_timestamp()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly["Date"], y=monthly["Amount"], mode="lines+markers",
                             name="المبيعات الفعلية" if ar else "Actual Sales"))
    fig.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecasted Sales"],
                             mode="lines+markers", line=dict(dash="dash"),
                             name="التوقعات" if ar else "Forecast"))
    fig.update_layout(title="توقع الإيرادات" if ar else "Revenue Forecast", template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)
