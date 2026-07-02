import streamlit as st


st.set_page_config(
    page_title="CFO AI PRO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    .stApp {
        background:
            radial-gradient(circle at 15% 15%, rgba(239,68,68,.16), transparent 30%),
            radial-gradient(circle at 85% 80%, rgba(59,130,246,.13), transparent 32%),
            linear-gradient(135deg, #07111f 0%, #101d33 52%, #07111f 100%);
    }
    .block-container {max-width: 980px; padding-top: 8vh;}
    .hero {text-align: center; color: white; padding: 3rem 1rem 2rem;}
    .brand-mark {
        display: inline-flex; width: 82px; height: 82px; align-items: center;
        justify-content: center; border-radius: 24px; font-size: 40px;
        background: linear-gradient(135deg, #ef4444, #dc2626);
        box-shadow: 0 20px 50px rgba(239,68,68,.28);
    }
    .hero h1 {font-size: 4rem; margin: 1.2rem 0 .3rem; color: white; letter-spacing: -.04em;}
    .hero .tagline {font-size: 1.3rem; color: #cbd5e1; margin: 0;}
    .hero .arabic {font-size: 1.05rem; color: #94a3b8; margin-top: .55rem;}
    .choice-title {text-align:center; color:#e2e8f0; font-size:1.05rem; margin:1.4rem 0 .5rem;}
    div[data-testid="stButton"] button {
        min-height: 72px; border-radius: 16px; font-size: 1.08rem; font-weight: 700;
        border: 1px solid rgba(255,255,255,.15); background: rgba(255,255,255,.08);
        color: white;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #ef4444; color: white; background: rgba(239,68,68,.18);
    }
    .trust {text-align:center; color:#64748b; margin-top:2.2rem; font-size:.9rem;}
    </style>
    <div class="hero">
        <div class="brand-mark">📊</div>
        <h1>CFO AI PRO</h1>
        <p class="tagline">Financial Intelligence for Smarter Business Decisions</p>
        <p class="arabic" dir="rtl">ذكاء مالي لقرارات أعمال أكثر ثقة</p>
    </div>
    <p class="choice-title">Choose your language &nbsp; • &nbsp; اختر لغتك</p>
    """,
    unsafe_allow_html=True,
)

arabic, english = st.columns(2, gap="medium")

with arabic:
    if st.button("🇸🇦  العربية", use_container_width=True):
        st.session_state.language = "ar"
        st.switch_page("pages/1_📊_Dashboard.py")

with english:
    if st.button("🇬🇧  English", use_container_width=True):
        st.session_state.language = "en"
        st.switch_page("pages/1_📊_Dashboard.py")

st.markdown(
    '<p class="trust">Secure analysis • Explainable insights • Human-led decisions</p>',
    unsafe_allow_html=True,
)
