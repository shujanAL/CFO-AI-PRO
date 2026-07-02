import streamlit as st
from utils.i18n import sar, tr


def show_executive_cards(metrics, health, forecast, language="en"):
    ar = language == "ar"
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🟢 الصحة المالية" if ar else "🟢 Financial Health", tr(health["status"], language), f'{health["score"]}/100')
    c2.metric("💰 الإيرادات" if ar else "💰 Revenue", sar(metrics["total_sales"], language))
    c3.metric("📈 صافي الربح" if ar else "📈 Net Profit", sar(metrics["net_profit"], language))
    trend = "Stable"
    if not forecast.empty and forecast.iloc[-1]["Forecasted Sales"] > forecast.iloc[0]["Forecasted Sales"]:
        trend = "Positive Outlook"
    elif not forecast.empty and forecast.iloc[-1]["Forecasted Sales"] < forecast.iloc[0]["Forecasted Sales"]:
        trend = "Needs Attention"
    c4.metric("🔮 التوقعات" if ar else "🔮 Forecast", tr(trend, language))
