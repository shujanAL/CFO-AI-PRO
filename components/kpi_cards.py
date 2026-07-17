import streamlit as st
from components.cards import show_card
from utils.i18n import sar, tr


def _delta(value, unit="%", positive_when_up=True):
    arrow = "↑" if value >= 0 else "↓"
    delta_type = "positive" if (value >= 0) == positive_when_up else "negative"
    return f"{arrow} {abs(value):.1f}{unit}", delta_type


def show_main_kpis(metrics, health, language="en", monthly_growth=0):
    ar = language == "ar"

    health_delta = health["score"] - 80
    health_delta_text, health_delta_type = _delta(health_delta, " pts")
    sales_delta_text, sales_delta_type = _delta(monthly_growth)
    profit_delta_text, profit_delta_type = _delta(metrics["profit_margin"])
    margin_delta_text, margin_delta_type = _delta(metrics["profit_margin"] - (metrics["expense_ratio"] * 100))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_card(
            "الصحة المالية" if ar else "Financial Health",
            f'{health["score"]}/100',
            "●",
            tr(health["status"], language),
            health_delta_text,
            health_delta_type,
        )
    with col2:
        show_card(
            "إجمالي المبيعات" if ar else "Total Sales",
            sar(metrics["total_sales"], language),
            "💰",
            "نمو المبيعات الشهري" if ar else "Monthly sales growth",
            sales_delta_text,
            sales_delta_type,
        )
    with col3:
        show_card(
            "صافي الربح" if ar else "Net Profit",
            sar(metrics["net_profit"], language),
            "📈",
            "بعد المصروفات" if ar else "After expenses",
            profit_delta_text,
            profit_delta_type,
        )
    with col4:
        show_card(
            "هامش الربح" if ar else "Profit Margin",
            f'{metrics["profit_margin"]:.1f}%',
            "📊",
            "الربحية مقابل المصروفات" if ar else "Profitability vs. expenses",
            margin_delta_text,
            margin_delta_type,
        )
