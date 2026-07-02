import pandas as pd

from engines.financial_score import calculate_financial_health


HEALTH_POINTS = {"Excellent": 100, "Good": 80, "Needs Attention": 55, "Critical": 25}


def _result(metrics, sales, expenses):
    profit = sales - expenses
    margin = (profit / sales * 100) if sales > 0 else 0
    expense_ratio = (expenses / sales) if sales > 0 else 0
    health = calculate_financial_health(margin, expense_ratio, metrics["overdue_ratio"])
    return profit, health


def rank_decisions(metrics, expenses_df=None):
    """Rank feasible scenarios using return, financial health, risk and confidence.

    The model uses transparent assumptions and is decision support, not a guarantee.
    """
    base_sales = float(metrics["total_sales"])
    base_expenses = float(metrics["total_expenses"])
    base_profit = float(metrics["net_profit"])
    candidates = []

    # Revenue growth has delivery/marketing costs. The 35% incremental-cost
    # assumption is deliberately visible in the UI and can later be company-specific.
    for pct in (5, 10, 15, 20):
        added_revenue = base_sales * pct / 100
        added_cost = added_revenue * 0.35
        sales = base_sales + added_revenue
        expenses = base_expenses + added_cost
        profit, health = _result(metrics, sales, expenses)
        risk = "Low" if pct <= 5 else "Moderate" if pct <= 10 else "High"
        confidence = "High" if pct <= 5 else "Medium" if pct <= 10 else "Low"
        candidates.append({
            "Decision": "Increase Sales",
            "Category": "Revenue",
            "Value": pct,
            "Expected Profit": round(profit),
            "Profit Change": round(profit - base_profit),
            "Health": health["status"],
            "Risk": risk,
            "Confidence": confidence,
            "Assumption": "35% of incremental revenue is required to deliver growth",
        })

    # Category reductions use the actual uploaded expense values, not all expenses.
    if expenses_df is not None and not expenses_df.empty:
        category_totals = expenses_df.groupby("Category")["Amount"].sum()
        for category, category_total in category_totals.items():
            for pct in (5, 10, 15):
                saving = float(category_total) * pct / 100
                profit, health = _result(metrics, base_sales, base_expenses - saving)
                risk = "Low" if pct <= 5 else "Moderate" if pct <= 10 else "High"
                candidates.append({
                    "Decision": "Reduce Expense",
                    "Category": category,
                    "Value": pct,
                    "Expected Profit": round(profit),
                    "Profit Change": round(profit - base_profit),
                    "Health": health["status"],
                    "Risk": risk,
                    "Confidence": "Medium",
                    "Assumption": f"Only the {category} category is reduced",
                })

    risk_penalty = {"Low": 0, "Moderate": 10, "High": 25}
    confidence_points = {"High": 100, "Medium": 70, "Low": 40}
    profit_scale = max(abs(base_profit), 1)
    for candidate in candidates:
        uplift = candidate["Profit Change"] / profit_scale
        candidate["Decision Score"] = round(
            min(100, max(0, 50 + uplift * 100)) * 0.50
            + HEALTH_POINTS[candidate["Health"]] * 0.30
            + confidence_points[candidate["Confidence"]] * 0.20
            - risk_penalty[candidate["Risk"]],
            1,
        )

    return pd.DataFrame(candidates).sort_values(
        ["Decision Score", "Expected Profit"], ascending=False
    ).reset_index(drop=True)
