import streamlit as st
from components.cards import show_card
from utils.i18n import sar, tr


def show_main_kpis(metrics, health, language="en"):
    ar = language == "ar"
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_card("الصحة المالية" if ar else "Financial Health", f'{health["score"]}/100', "🟢", tr(health["status"], language))
    with col2:
        show_card("إجمالي المبيعات" if ar else "Total Sales", sar(metrics["total_sales"], language), "💰", "إجمالي الإيرادات" if ar else "Total revenue")
    with col3:
        show_card("صافي الربح" if ar else "Net Profit", sar(metrics["net_profit"], language), "📈", "بعد المصروفات" if ar else "After expenses")
    with col4:
        show_card("هامش الربح" if ar else "Profit Margin", f'{metrics["profit_margin"]:.1f}%', "📊", "الربحية" if ar else "Profitability")
