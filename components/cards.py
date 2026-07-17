import streamlit as st


def show_card(title, value, icon="📊", subtitle="", delta=None, delta_type="positive"):
    delta_html = ""
    if delta:
        delta_class = "positive" if delta_type == "positive" else "negative"
        delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>'

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
            <div class="metric-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
