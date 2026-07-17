import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.i18n import tr


CFO_CHART_COLORS = ["#5b1235", "#2b183f", "#b88954", "#8a3d5d", "#22745f", "#d8b889"]


def apply_cfo_chart_theme(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(family="Arial, Tahoma, sans-serif", color="#211827"),
        title=dict(font=dict(size=20, color="#2b183f")),
        margin=dict(l=14, r=14, t=48, b=24),
        colorway=CFO_CHART_COLORS,
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color="#706777")),
    )
    fig.update_xaxes(
        gridcolor="#eee7dd",
        zerolinecolor="#eee7dd",
        linecolor="#e7ded2",
        tickfont=dict(color="#706777"),
    )
    fig.update_yaxes(
        gridcolor="#eee7dd",
        zerolinecolor="#eee7dd",
        linecolor="#e7ded2",
        tickfont=dict(color="#706777"),
    )
    return fig


def show_monthly_sales_chart(sales_df, language="en"):
    ar = language == "ar"
    df = sales_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly["Date"] = monthly["Date"].astype(str)
    fig = px.line(
        monthly,
        x="Date",
        y="Amount",
        markers=True,
        title="اتجاه الإيرادات الشهرية" if ar else "Monthly Revenue Trend",
        labels={"Date": "الشهر" if ar else "Date", "Amount": "المبلغ" if ar else "Amount"},
    )
    fig.update_traces(line=dict(color="#5b1235", width=3), marker=dict(size=8, color="#b88954"))
    apply_cfo_chart_theme(fig, height=470)
    st.plotly_chart(fig, use_container_width=True)


def show_expense_breakdown(expenses_df, language="en"):
    ar = language == "ar"
    category = expenses_df.groupby("Category")["Amount"].sum().reset_index()
    if ar:
        category["Category"] = category["Category"].map(lambda value: tr(value, language))
    fig = px.pie(
        category,
        names="Category",
        values="Amount",
        hole=0.45,
        title="توزيع المصروفات" if ar else "Expense Breakdown",
        color_discrete_sequence=CFO_CHART_COLORS,
    )
    fig.update_traces(textfont=dict(color="#211827"), marker=dict(line=dict(color="#ffffff", width=2)))
    apply_cfo_chart_theme(fig, height=470)
    st.plotly_chart(fig, use_container_width=True)


def show_forecast_chart(history_df, forecast_df, language="en"):
    ar = language == "ar"
    history = history_df.copy()
    history["Date"] = pd.to_datetime(history["Date"])
    monthly = history.groupby(history["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly["Date"] = monthly["Date"].dt.to_timestamp()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["Date"],
            y=monthly["Amount"],
            mode="lines+markers",
            line=dict(color="#5b1235", width=3),
            marker=dict(size=8, color="#b88954"),
            name="المبيعات الفعلية" if ar else "Actual Sales",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Forecasted Sales"],
            mode="lines+markers",
            line=dict(dash="dash", color="#2b183f", width=3),
            marker=dict(size=8, color="#2b183f"),
            name="التوقعات" if ar else "Forecast",
        )
    )
    fig.update_layout(title="توقع الإيرادات" if ar else "Revenue Forecast")
    apply_cfo_chart_theme(fig, height=480)
    st.plotly_chart(fig, use_container_width=True)
