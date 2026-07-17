import pandas as pd
import streamlit as st

from components.history import save_history
from engines.decision_engine import simulate_decision, update_expense_category
from engines.financial_score import calculate_financial_health
from engines.simulation_ai import generate_simulation_analysis
from utils.i18n import sar, tr


def show_decision_simulator(metrics, health, expenses_df, language="en"):
    ar = language == "ar"
    label = lambda en, ar_text: ar_text if ar else en
    fmt = lambda value: tr(value, language)

    def percentage_change_slider(key):
        st.markdown(
            f'<div class="cfo-slider-label">{label("Percentage Change (%)", "نسبة التغيير (%)")}</div>',
            unsafe_allow_html=True,
        )
        return st.slider(
            label("Percentage Change (%)", "نسبة التغيير (%)"),
            min_value=0,
            max_value=100,
            value=10,
            step=1,
            key=key,
            label_visibility="collapsed",
        )

    st.divider()
    st.subheader(label("🧮 CFO Decision Simulator", "🧮 محاكي قرارات المدير المالي"))
    st.caption(label(
        "Test a financial move before applying it to the company.",
        "اختبر أثر القرار المالي قبل تطبيقه على الشركة.",
    ))

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="cfo-simulator-intro">
                <span class="cfo-simulator-badge">CFO Calculator</span>
                <strong>{label("Scenario controls", "إعدادات السيناريو")}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
        scenario_type = st.selectbox(
            label("Decision Type", "نوع القرار"),
            ["Revenue", "Expenses", "Employees"], format_func=fmt,
        )
        action = category = department = position = None
        percentage, salary, employee_count = 0, 0, 1

        if scenario_type == "Revenue":
            left, right = st.columns([1, 1])
            with left:
                action = st.selectbox(label("Scenario", "السيناريو"), ["Increase Sales", "Decrease Sales"], format_func=fmt)
            with right:
                st.markdown("&nbsp;", unsafe_allow_html=True)
            percentage = percentage_change_slider("revenue_percentage_change")
        elif scenario_type == "Expenses":
            col1, col2 = st.columns([1, 1])
            with col1:
                category = st.selectbox(label("Expense Category", "فئة المصروف"),
                                        ["Salaries", "Marketing", "Inventory", "Rent", "Utilities", "Software"], format_func=fmt)
            with col2:
                action = st.selectbox(label("Scenario", "السيناريو"), ["Increase Expense", "Reduce Expense"], format_func=fmt)
            percentage = percentage_change_slider("expense_percentage_change")
        else:
            col1, col2 = st.columns(2)
            with col1:
                action = st.selectbox(label("Scenario", "السيناريو"), ["Hire Employee", "Lay Off Employee"], format_func=fmt)
                department = st.selectbox(label("Department", "الإدارة"), ["Sales", "Finance", "Marketing", "Operations", "Support"], format_func=fmt)
                employee_count = st.number_input(label("Number of Employees", "عدد الموظفين"), min_value=1, value=1, step=1)
            with col2:
                position = st.selectbox(label("Position", "المسمى الوظيفي"),
                                        ["Data Analyst", "Accountant", "Sales Representative", "Marketing Specialist", "Operations Coordinator", "Customer Support"], format_func=fmt)
                salary = st.number_input(label("Monthly Salary (SAR)", "الراتب الشهري (ر.س)"), min_value=1000, value=8000, step=500)

        run_simulation = st.button(label("🚀 Run Simulation", "🚀 تشغيل المحاكاة"), use_container_width=True)

    if not run_simulation:
        return

    if scenario_type == "Expenses":
        updated = update_expense_category(expenses_df, category, action, percentage)
        new_expenses = updated["Amount"].sum()
        new_sales = metrics["total_sales"]
        new_profit = new_sales - new_expenses
        margin = (new_profit / new_sales * 100) if new_sales else 0
        ratio = (new_expenses / new_sales) if new_sales else 0
        new_health = calculate_financial_health(margin, ratio, metrics["overdue_ratio"])
        result = {"new_sales": new_sales, "new_expenses": new_expenses, "new_profit": new_profit,
                  "new_profit_margin": margin, "new_health_score": new_health["score"],
                  "new_health_status": new_health["status"]}
    else:
        result = simulate_decision(metrics, scenario_type, action, category, percentage, salary, employee_count)

    analysis = generate_simulation_analysis(scenario_type, action, result, metrics["net_profit"], language)
    keys = (["نوع القرار", "الإجراء", "الفئة", "الربح قبل", "الربح بعد", "الصحة قبل", "الصحة بعد"]
            if ar else ["Decision Type", "Action", "Category", "Before Profit", "After Profit", "Before Health", "After Health"])
    save_history(dict(zip(keys, [fmt(scenario_type), fmt(action), fmt(category) if category else label("N/A", "لا ينطبق"),
                                  sar(metrics["net_profit"], language), sar(result["new_profit"], language),
                                  f'{health["score"]}/100', f'{result["new_health_score"]}/100'])))

    names = (["المبيعات", "المصروفات", "صافي الربح", "هامش الربح", "الصحة المالية"]
             if ar else ["Sales", "Expenses", "Net Profit", "Profit Margin", "Financial Health"])
    comparison = pd.DataFrame({
        label("Metric", "المؤشر"): names,
        label("Before", "قبل"): [sar(metrics["total_sales"], language), sar(metrics["total_expenses"], language),
                                    sar(metrics["net_profit"], language), f'{metrics["profit_margin"]:.1f}%', f'{health["score"]}/100'],
        label("After", "بعد"): [sar(result["new_sales"], language), sar(result["new_expenses"], language),
                                  sar(result["new_profit"], language), f'{result["new_profit_margin"]:.1f}%', f'{result["new_health_score"]}/100'],
    })
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    st.markdown(analysis)
    if scenario_type == "Employees":
        st.info(label(
            f"Department: {department} • Position: {position} • Employees: {employee_count}",
            f"الإدارة: {fmt(department)} • الوظيفة: {fmt(position)} • عدد الموظفين: {employee_count}",
        ))
