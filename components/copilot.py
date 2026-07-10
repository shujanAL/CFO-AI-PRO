import pandas as pd
import streamlit as st

from engines.local_ai import ask_local_ai, is_ollama_available
from engines.rule_based_copilot import ask_rule_based_copilot


EXAMPLE_QUESTIONS_EN = [
    "Why is my Financial Health score this level?",
    "Should I hire 3 employees?",
    "What is my biggest financial risk?",
    "Which expense should I reduce first?",
    "Can I apply for financing?",
]

EXAMPLE_QUESTIONS_AR = [
    "ليش درجة الصحة المالية بهذا المستوى؟",
    "هل أوظف 3 موظفين؟",
    "ما هو أكبر خطر مالي؟",
    "أي مصروف أخفض أولاً؟",
    "هل أقدر أقدم على تمويل؟",
]


def _df_to_records(df, limit=5):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return []
    return df.head(limit).to_dict(orient="records")


def _row_to_dict(row):
    if row is None:
        return {}
    if hasattr(row, "to_dict"):
        return row.to_dict()
    if isinstance(row, dict):
        return row
    return {}


def build_copilot_context(metrics, health, forecast, ranking, best_decision, financing, recommendation):
    history = st.session_state.get("history", [])
    return {
        "metrics": metrics,
        "health": health,
        "forecast": _df_to_records(forecast, limit=6),
        "top_decisions": _df_to_records(ranking, limit=10),
        "best_decision": _row_to_dict(best_decision),
        "financing": financing,
        "recommendation": recommendation,
        "decision_history": history[-10:] if isinstance(history, list) else [],
    }


def show_financial_copilot(metrics, health, forecast, ranking, best_decision, financing, recommendation, language="en"):
    is_ar = language == "ar"
    st.subheader("💬 المساعد المالي CFO AI" if is_ar else "💬 Financial Copilot")
    st.caption(
        "يسأل عن التحليل الحالي فقط. إذا كان Ollama يعمل محليًا يستخدم Local AI، وإذا لم يعمل يستخدم مساعدًا منطقيًا مبنيًا على القواعد."
        if is_ar
        else "Ask about the current analysis only. Uses Local AI when Ollama is running, otherwise falls back to a rule-based financial copilot."
    )

    available = is_ollama_available()
    if available:
        st.success("Local AI is active via Ollama." if not is_ar else "Local AI يعمل عبر Ollama.")
    else:
        st.warning(
            "Ollama is not running, so CFO AI is using Rule-based Copilot mode."
            if not is_ar
            else "Ollama غير شغال، لذلك يعمل CFO AI بوضع Rule-based Copilot."
        )

    examples = EXAMPLE_QUESTIONS_AR if is_ar else EXAMPLE_QUESTIONS_EN
    selected = st.selectbox(
        "أسئلة جاهزة" if is_ar else "Example questions",
        [""] + examples,
        index=0,
    )
    question = st.text_area(
        "Ask CFO AI" if not is_ar else "اسأل CFO AI",
        value=selected or "",
        placeholder=examples[0],
        height=90,
    )

    if st.button("Ask CFO AI" if not is_ar else "اسأل CFO AI"):
        if not question.strip():
            st.error("Write a question first." if not is_ar else "اكتب السؤال أولاً.")
            return

        context = build_copilot_context(metrics, health, forecast, ranking, best_decision, financing, recommendation)
        answer, source, error = ask_local_ai(question.strip(), context, language=language)
        if answer is None:
            answer = ask_rule_based_copilot(question.strip(), context, language=language)
            source = "Rule-based Copilot"

        st.markdown(answer)
        st.caption(f"Answer source: {source}" if not is_ar else f"مصدر الإجابة: {source}")
        if error and source == "Rule-based Copilot":
            st.caption(error)
