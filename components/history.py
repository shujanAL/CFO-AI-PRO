import pandas as pd
import streamlit as st


def save_history(record):
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(record)


def show_history(language="en"):
    ar = language == "ar"
    st.subheader("📜 سجل القرارات" if ar else "📜 Decision History")
    if not st.session_state.get("history"):
        st.info("لا توجد محاكاة محفوظة حتى الآن." if ar else "No simulations yet.")
        return
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("🗑 مسح السجل" if ar else "🗑 Clear History"):
        st.session_state.history = []
        st.rerun()
