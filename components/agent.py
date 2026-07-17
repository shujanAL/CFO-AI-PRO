import streamlit as st

from components.copilot import build_copilot_context
from engines.local_ai import ask_local_ai, is_ollama_available
from engines.rule_based_copilot import ask_rule_based_copilot, is_verified_financial_question
from utils.finance_text import finance_text, trend_text
from utils.i18n import sar, tr


def _forecast_trend(forecast):
    if forecast is None or forecast.empty or len(forecast) < 2:
        return "Stable"
    first = float(forecast.iloc[0]["Forecasted Sales"])
    last = float(forecast.iloc[-1]["Forecasted Sales"])
    if last > first:
        return "Growing"
    if last < first:
        return "Declining"
    return "Stable"


def _agent_summary(metrics, health, financing, forecast, best_decision, language="en"):
    is_ar = language == "ar"
    trend = _forecast_trend(forecast)
    displayed_trend = trend_text(trend, language)
    if is_ar:
        return f"""
### نتيجة CFO AI Agent

- تم قراءة بيانات الشركة والتحقق منها.
- الصحة المالية: **{health.get("score", 0)}/100 - {tr(health.get("status", ""), language)}**
- جاهزية التمويل البنكي: **{financing.get("score", 0)}/100 - Grade {financing.get("grade", "N/A")}**
- اتجاه التوقعات: **{displayed_trend}**
- أفضل قرار مقترح: **{tr(best_decision.get("Decision", "N/A"), language)}**
- الربح المتوقع بعد القرار: **{sar(best_decision.get("Expected Profit", 0), language)}**

النصيحة: ابدأ بتنفيذ القرار كتجربة محدودة، ثم راقب الربح والتحصيل والمصروفات قبل التوسع.
"""
    return f"""
### CFO AI Agent Result

- Company data was loaded and validated.
- Financial Health: **{health.get("score", 0)}/100 - {health.get("status", "N/A")}**
- Bank Financing Readiness: **{financing.get("score", 0)}/100 - Grade {financing.get("grade", "N/A")}**
- Forecast trend: **{trend}**
- Recommended decision: **{best_decision.get("Decision", "N/A")}**
- Expected profit after scenario: **{sar(best_decision.get("Expected Profit", 0), language)}**

Advice: run the recommendation as a controlled pilot, then monitor profit, collections, and expenses before scaling.
"""


def show_cfo_agent(metrics, health, financing, forecast, ranking, best_decision, recommendation, language="en"):
    is_ar = language == "ar"
    st.subheader("🤖 CFO AI Agent")
    st.caption(
        "One-click agent that validates the company data, reads the analysis, ranks scenarios, explains financing readiness, and answers management questions."
        if not is_ar
        else "وكيل ذكي بضغطة واحدة يقرأ بيانات الشركة، يحلل الوضع، يرتب السيناريوهات، يشرح الجاهزية التمويلية، ويجيب على أسئلة الإدارة."
    )

    steps = [
        ("Validate Excel", "تحقق من Excel"),
        ("Analyze financial metrics", "تحليل المؤشرات المالية"),
        ("Calculate Financial Health", "حساب الصحة المالية"),
        ("Calculate Bank Financing Readiness", "حساب الجاهزية التمويلية"),
        ("Run sales forecast", "تشغيل التوقعات"),
        ("Rank decision scenarios", "ترتيب السيناريوهات"),
        ("Generate executive recommendation", "إنشاء توصية تنفيذية"),
    ]

    request = st.text_input(
        "Agent request" if not is_ar else "طلب الوكيل",
        placeholder=(
            "Example: What should management do in the next 30 days?"
            if not is_ar
            else "مثال: ماذا يجب على الإدارة أن تفعل خلال 30 يوم؟"
        ),
    )

    if st.button("🚀 Run CFO AI Agent" if not is_ar else "🚀 تشغيل وكيل CFO AI"):
        for english, arabic in steps:
            st.success(("✅ " + english) if not is_ar else ("✅ " + arabic))

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Financial Health" if not is_ar else "الصحة المالية", f'{health.get("score", 0)}/100', tr(health.get("status", ""), language))
        c2.metric("Financing Readiness" if not is_ar else "الجاهزية التمويلية", f'{financing.get("score", 0)}/100', f'Grade {financing.get("grade", "N/A")}')
        c3.metric("Expected Profit" if not is_ar else "الربح المتوقع", sar(best_decision.get("Expected Profit", 0), language))
        c4.metric("Best Decision" if not is_ar else "أفضل قرار", tr(best_decision.get("Decision", "N/A"), language))

        st.markdown(_agent_summary(metrics, health, financing, forecast, best_decision, language))

        with st.expander("Financing blockers and improvement plan" if not is_ar else "عوائق التمويل وخطة التحسين", expanded=True):
            st.markdown("**What may prevent financing:**" if not is_ar else "**ما الذي قد يمنع التمويل:**")
            for blocker in financing.get("blockers", []):
                st.write(f"- {finance_text(blocker, language)}")
            st.markdown("**How to improve the score:**" if not is_ar else "**كيف يمكن رفع الدرجة:**")
            for action in financing.get("improvement_actions", []):
                st.write(f"- {finance_text(action, language)}")

        if request.strip():
            context = build_copilot_context(metrics, health, forecast, ranking, best_decision, financing, recommendation)
            if is_verified_financial_question(request.strip()):
                answer = ask_rule_based_copilot(request.strip(), context, language=language)
                source = "Verified Financial Engine"
            else:
                answer, source, _error = ask_local_ai(request.strip(), context, language=language)
                if answer is None:
                    answer = ask_rule_based_copilot(request.strip(), context, language=language)
                    source = "Rule-based Agent"
            st.markdown(answer)
            st.caption(("Answer source: " if not is_ar else "مصدر الإجابة: ") + source)
        else:
            st.info(
                "Ollama Local AI is active." if is_ollama_available() and not is_ar else
                "Local AI يعمل عبر Ollama." if is_ollama_available() and is_ar else
                "Local AI is not running here, so the agent uses the rule-based financial engine safely."
                if not is_ar else
                "Local AI غير شغال هنا، لذلك يستخدم الوكيل محركًا ماليًا مبنيًا على القواعد بشكل آمن."
            )
