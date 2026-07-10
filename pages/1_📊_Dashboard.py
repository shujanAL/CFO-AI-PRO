import streamlit as st
import pandas as pd
import plotly.express as px
from components.history import show_history
from engines.executive_summary import generate_executive_summary
from components.executive_cards import show_executive_cards
from engines.decision_ranking import rank_decisions
from engines.recommendation_engine import generate_recommendation
from report.pdf_report import generate_pdf

from engines.ai_advisor import generate_ai_summary
from engines.forecast_engine import forecast_monthly_sales
from engines.financial_metrics import (
    calculate_basic_metrics,
    calculate_average_invoice,
    calculate_monthly_sales,
    calculate_monthly_growth,
)
from engines.financial_score import calculate_financial_health
import engines.financial_score

from components.kpi_cards import show_main_kpis
from components.charts import show_forecast_chart
from components.simulator import show_decision_simulator
from components.copilot import show_financial_copilot
from engines.financing_readiness import calculate_financing_readiness
from utils.import_engine import validate_excel
from utils.i18n import sar, tr


st.set_page_config(page_title="CFO AI Dashboard", layout="wide")

language = st.session_state.get("language", "en")
is_arabic = language == "ar"

if is_arabic:
    st.markdown(
        """<style>
        .stMainBlockContainer, [data-testid="stSidebarContent"] {direction: rtl; text-align: right;}
        [data-testid="stMetric"] {text-align: right;}
        </style>""",
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.caption("اللغة / Language")
    selected_language = st.radio(
        "Language",
        ["العربية", "English"],
        index=0 if is_arabic else 1,
        label_visibility="collapsed",
    )
    new_language = "ar" if selected_language == "العربية" else "en"
    if new_language != language:
        st.session_state.language = new_language
        st.rerun()


def load_css():
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_monthly_sales_chart(sales_df):
    df = sales_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    monthly = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
        .reset_index()
    )

    monthly["Date"] = monthly["Date"].astype(str)

    fig = px.line(
        monthly,
        x="Date",
        y="Amount",
        markers=True,
        title="اتجاه الإيرادات الشهرية" if is_arabic else "Monthly Revenue Trend",
        labels={"Date": "الشهر" if is_arabic else "Date", "Amount": "المبلغ" if is_arabic else "Amount"},
    )

    fig.update_layout(height=420, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)


def show_expense_breakdown(expenses_df):
    category = (
        expenses_df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )
    if is_arabic:
        category["Category"] = category["Category"].map(lambda value: tr(value, language))

    fig = px.pie(
        category,
        names="Category",
        values="Amount",
        hole=0.45,
        title="توزيع المصروفات" if is_arabic else "Expense Breakdown"
    )

    fig.update_layout(height=420, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)


load_css()

st.title("📊 لوحة CFO AI للتحليل المالي" if is_arabic else "📊 CFO AI Dashboard")
st.caption(
    "من بيانات الشركة إلى قرارات مالية وتمويلية قابلة للتفسير خلال دقائق."
    if is_arabic
    else "From company data to explainable financial and financing decisions in minutes."
)

uploaded_file = st.file_uploader(
    "ارفع ملف Excel الخاص بالشركة" if is_arabic else "Upload Company Excel File",
    type=["xlsx"]
)

excel_file = uploaded_file if uploaded_file is not None else "templates/sample_company_data.xlsx"
is_valid, validation_message = validate_excel(excel_file)

if not is_valid:
    st.error((f"ملف Excel غير متوافق: {validation_message}" if is_arabic else f"The uploaded workbook is not compatible: {validation_message}"))
    st.info("استخدم قالب CFO AI وحافظ على أسماء الصفحات والأعمدة المطلوبة." if is_arabic else "Use the CFO AI template and keep the required sheet and column names.")
    st.stop()
elif uploaded_file is not None:
    st.success("تم التحقق من ملف الشركة وتحميله بنجاح." if is_arabic else "Company file validated and loaded successfully.")
else:
    st.info("وضع العرض: تُستخدم بيانات شركة تجريبية. ارفع ملف Excel لتحليل شركتك." if is_arabic else "Demo mode: using sample company data. Upload an Excel file to analyze your company.")

try:
    sales = pd.read_excel(excel_file, sheet_name="Sales")
    expenses = pd.read_excel(excel_file, sheet_name="Expenses")
    invoices = pd.read_excel(excel_file, sheet_name="Invoices")
except Exception as error:
    st.error(f"تعذر قراءة البيانات المالية: {error}" if is_arabic else f"Could not read the financial data: {error}")
    st.stop()

metrics = calculate_basic_metrics(sales, expenses, invoices)

health = calculate_financial_health(
    metrics["profit_margin"],
    metrics["expense_ratio"],
    metrics["overdue_ratio"]
)

show_main_kpis(metrics, health, language)

st.divider()

st.subheader("🏦 الجاهزية للتمويل البنكي" if is_arabic else "🏦 Bank Financing Readiness")
financing = calculate_financing_readiness(metrics, health)
f1, f2, f3, f4 = st.columns(4)
f1.metric("درجة الجاهزية" if is_arabic else "Readiness Score", f'{financing["score"]}/100')
f2.metric("التصنيف الائتماني" if is_arabic else "Credit Grade", financing["grade"])
f3.metric("مستوى المخاطر" if is_arabic else "Risk Level", tr(financing["risk"], language))
f4.metric("الحد التمويلي الإرشادي" if is_arabic else "Indicative Limit", sar(financing["suggested_limit"], language))

st.progress(financing["score"] / 100)
st.info(tr(financing["recommendation"], language))
with st.expander("لماذا حصلت الشركة على هذه الدرجة؟" if is_arabic else "Why did the company receive this score?"):
    factor_df = pd.DataFrame(
        financing["factors"],
        columns=(["العامل", "النقاط", "الحد الأعلى", "التفسير"] if is_arabic else ["Factor", "Points", "Maximum", "Explanation"]),
    )
    if is_arabic:
        factor_df["العامل"] = factor_df["العامل"].map(lambda value: tr(value, language))
        factor_df["التفسير"] = [
            f'هامش الربح {metrics["profit_margin"]:.1f}%',
            f'نسبة المصروفات {metrics["expense_ratio"]:.1%}',
            f'نسبة الفواتير المتأخرة {metrics["overdue_ratio"]:.1%}',
            f'درجة الصحة المالية {health["score"]}/100',
        ]
    st.dataframe(factor_df, use_container_width=True, hide_index=True)
    st.caption(
        ("هذا مؤشر داعم للقرار فقط. قرار الائتمان النهائي يتطلب مراجعة بشرية ومستندات إضافية."
         if is_arabic else "Decision-support indicator only. Final credit decisions require human review and additional documents.")
    )

st.divider()

st.subheader("مؤشرات الأعمال" if is_arabic else "Business Metrics")

c1, c2, c3 = st.columns(3)

c1.metric("متوسط قيمة الفاتورة" if is_arabic else "Average Invoice", sar(calculate_average_invoice(invoices), language))
c2.metric("متوسط المبيعات الشهرية" if is_arabic else "Average Monthly Sales", sar(calculate_monthly_sales(sales), language))

growth = calculate_monthly_growth(sales)
c3.metric("النمو الشهري" if is_arabic else "Monthly Growth", f"{growth:.2f}%")

st.divider()

st.subheader("الحالة المالية" if is_arabic else "Financial Status")

if health["status"] == "Excellent":
    st.success(("الحالة الحالية: " if is_arabic else "Current Status: ") + tr(health["status"], language))
elif health["status"] == "Good":
    st.info(("الحالة الحالية: " if is_arabic else "Current Status: ") + tr(health["status"], language))
elif health["status"] == "Warning":
    st.warning(("الحالة الحالية: " if is_arabic else "Current Status: ") + tr(health["status"], language))
else:
    st.error(("الحالة الحالية: " if is_arabic else "Current Status: ") + tr(health["status"], language))

st.divider()

st.subheader("تحليلات الأعمال" if is_arabic else "Business Analytics")

left, right = st.columns(2)

with left:
    show_monthly_sales_chart(sales)

with right:
    show_expense_breakdown(expenses)

st.divider()

st.subheader("🤖 المستشار المالي الذكي" if is_arabic else "🤖 AI Financial Advisor")

summary = generate_ai_summary(metrics, language)

for item in summary:
    st.info(item)

st.divider()

st.subheader("🔮 توقع المبيعات" if is_arabic else "🔮 Sales Forecast")

forecast = forecast_monthly_sales(sales, months_ahead=3)
show_forecast_chart(sales, forecast, language)
st.divider()


st.divider()

st.subheader("📋 الملخص التنفيذي" if is_arabic else "📋 Executive Summary")

show_executive_cards(metrics, health, forecast, language)

show_decision_simulator(metrics, health, expenses, language)
show_history(language)


st.divider()

st.subheader("🏆 ترتيب القرارات الذكي" if is_arabic else "🏆 AI Decision Ranking")

ranking = rank_decisions(metrics, expenses)

ranking_display = ranking.copy()
if is_arabic:
    ranking_display["Decision"] = ranking_display["Decision"].map(lambda value: tr(value, language))
    ranking_display["Category"] = ranking_display["Category"].map(lambda value: tr(value, language))
    ranking_display["Health"] = ranking_display["Health"].map(lambda value: tr(value, language))
    ranking_display["Risk"] = ranking_display["Risk"].map(lambda value: tr(value, language))
    ranking_display["Confidence"] = ranking_display["Confidence"].map({"High": "عالية", "Medium": "متوسطة", "Low": "منخفضة"})
    ranking_display["Assumption"] = ranking.apply(
        lambda row: (
            "يفترض أن 35% من الإيراد الإضافي يغطي تكلفة تحقيق النمو"
            if row["Decision"] == "Increase Sales"
            else f'يتم خفض فئة {tr(row["Category"], language)} فقط'
        ), axis=1
    )
    ranking_display = ranking_display.rename(columns={"Decision": "القرار", "Category": "الفئة", "Value": "القيمة", "Expected Profit": "الربح المتوقع", "Profit Change": "تغير الربح", "Health": "الصحة المالية", "Risk": "المخاطر", "Confidence": "الثقة", "Assumption": "الافتراض", "Decision Score": "درجة القرار"})
st.dataframe(ranking_display.head(10), use_container_width=True)

best_decision = ranking.iloc[0]
confidence_ar = {"High": "عالية", "Medium": "متوسطة", "Low": "منخفضة"}.get(
    best_decision["Confidence"], best_decision["Confidence"]
)

if is_arabic:
    st.success(f"""
🏆 أفضل قرار: **{tr(best_decision["Decision"], language)}**

الفئة: **{tr(best_decision["Category"], language)}**

القيمة: **{best_decision["Value"]}%**

الربح المتوقع: **{sar(best_decision["Expected Profit"], language)}**

الصحة المالية: **{tr(best_decision["Health"], language)}**

المخاطر: **{tr(best_decision["Risk"], language)}** | الثقة: **{confidence_ar}**
""")
else:
    st.success(f"""
🏆 Best Decision: **{best_decision["Decision"]}**

Category: **{best_decision["Category"]}**

Value: **{best_decision["Value"]}%**

Expected Profit: **{sar(best_decision["Expected Profit"])}**

Financial Health: **{best_decision["Health"]}**

Risk: **{best_decision["Risk"]}** | Confidence: **{best_decision["Confidence"]}**
""")

recommendation = generate_recommendation(best_decision, metrics, language)

st.info(recommendation)

st.divider()

show_financial_copilot(metrics, health, forecast, ranking, best_decision, financing, recommendation, language)

st.divider()

st.subheader("📄 التقرير التنفيذي" if is_arabic else "📄 Executive Report")

if st.button("إنشاء التقرير التنفيذي" if is_arabic else "Generate Executive Report"):
    pdf_path = generate_pdf(metrics, health, best_decision)

    with open(pdf_path, "rb") as file:
        st.download_button(
            label="⬇️ تنزيل تقرير PDF" if is_arabic else "⬇️ Download PDF Report",
            data=file,
            file_name="CFO_AI_Executive_Report.pdf",
            mime="application/pdf"
        )
