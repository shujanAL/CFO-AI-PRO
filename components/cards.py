import streamlit as st


def show_card(title, value, icon="📊", subtitle=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size:28px;">{icon}</div>
            <div style="font-size:15px; color:#6B7280; margin-top:8px;">
                {title}
            </div>
            <div style="font-size:32px; font-weight:700; color:#16213E; margin-top:8px;">
                {value}
            </div>
            <div style="font-size:13px; color:#6B7280; margin-top:6px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )