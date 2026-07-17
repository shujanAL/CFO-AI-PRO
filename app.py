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
    :root {
        --cfo-bg: #fbfaf7;
        --cfo-burgundy: #5b1235;
        --cfo-burgundy-2: #711944;
        --cfo-purple: #2b183f;
        --cfo-gold: #b88954;
        --cfo-muted: #706777;
        --cfo-border: #e7ded2;
    }
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHeader"] {background: transparent;}
    .stApp {
        background:
            radial-gradient(circle at 12% 12%, rgba(91,18,53,.10), transparent 30%),
            radial-gradient(circle at 84% 78%, rgba(184,137,84,.18), transparent 28%),
            linear-gradient(135deg, #fffdf9 0%, #fbfaf7 50%, #f3efe8 100%);
    }
    .block-container {max-width: 1040px; padding-top: 8vh;}
    .hero {
        position: relative;
        overflow: hidden;
        text-align: center;
        padding: 3.2rem 2rem 2.6rem;
        border-radius: 34px;
        background: rgba(255,255,255,.82);
        border: 1px solid rgba(91,18,53,.10);
        box-shadow: 0 24px 70px rgba(43,24,63,.10);
    }
    .brand-mark {
        display: inline-flex;
        width: 86px;
        height: 86px;
        align-items: center;
        justify-content: center;
        border-radius: 28px;
        font-size: 42px;
        background: linear-gradient(135deg, var(--cfo-burgundy), var(--cfo-purple));
        box-shadow: 0 20px 50px rgba(91,18,53,.24);
        color: white;
    }
    .hero h1 {
        font-size: clamp(2.7rem, 6vw, 4.5rem);
        margin: 1.15rem 0 .3rem;
        color: var(--cfo-purple);
        letter-spacing: -.05em;
        font-weight: 900;
    }
    .hero .tagline {font-size: 1.26rem; color: var(--cfo-muted); margin: 0;}
    .hero .arabic {font-size: 1.05rem; color: var(--cfo-burgundy); margin-top: .55rem;}
    .choice-title {text-align:center; color:var(--cfo-purple); font-weight:800; font-size:1.05rem; margin:1.4rem 0 .5rem;}
    div[data-testid="stButton"] button {
        min-height: 72px;
        border-radius: 999px;
        font-size: 1.08rem;
        font-weight: 800;
        border: 1px solid rgba(91,18,53,.18);
        background: linear-gradient(135deg, var(--cfo-burgundy), var(--cfo-burgundy-2));
        color: white;
        box-shadow: 0 14px 30px rgba(91,18,53,.18);
        transition: transform .16s ease, box-shadow .16s ease, filter .16s ease;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        filter: brightness(1.04);
        box-shadow: 0 18px 40px rgba(91,18,53,.25);
        color: white;
    }
    .trust {text-align:center; color:#7d7482; margin-top:2.2rem; font-size:.92rem;}
    @media (max-width: 768px) {
        .block-container {padding-top: 3vh;}
        .hero {padding: 2rem 1rem; border-radius: 26px;}
    }
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
    '<p class="trust">Private analysis • Explainable insights • Human-led decisions</p>',
    unsafe_allow_html=True,
)
