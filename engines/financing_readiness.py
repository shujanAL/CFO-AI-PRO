"""Explainable financing-readiness assessment for hackathon demonstrations.

This score supports a human credit review; it is not an automated lending decision.
"""


def calculate_financing_readiness(metrics, health):
    score = 0
    factors = []

    margin = float(metrics.get("profit_margin", 0))
    expense_ratio = float(metrics.get("expense_ratio", 0))
    overdue_ratio = float(metrics.get("overdue_ratio", 0))
    profit = float(metrics.get("net_profit", 0))

    profitability = max(0, min(30, round((margin / 30) * 30)))
    score += profitability
    factors.append(("Profitability", profitability, 30, f"Profit margin is {margin:.1f}%"))

    efficiency = max(0, min(25, round((1 - expense_ratio) * 25)))
    score += efficiency
    factors.append(("Cost efficiency", efficiency, 25, f"Expense ratio is {expense_ratio:.1%}"))

    collections = max(0, min(25, round((1 - overdue_ratio) * 25)))
    score += collections
    factors.append(("Collections", collections, 25, f"Overdue invoices are {overdue_ratio:.1%}"))

    stability = round(float(health.get("score", 0)) * 0.20)
    score += stability
    factors.append(("Financial stability", stability, 20, f"Health score is {health.get('score', 0)}/100"))

    score = max(0, min(100, round(score)))
    if score >= 80:
        grade, risk, recommendation = "A", "Low", "Ready for financing review"
    elif score >= 65:
        grade, risk, recommendation = "B", "Moderate", "Conditionally ready"
    elif score >= 50:
        grade, risk, recommendation = "C", "Elevated", "Needs additional review"
    else:
        grade, risk, recommendation = "D", "High", "Not ready yet"

    suggested_limit = max(0, min(metrics.get("total_sales", 0) * 0.20, profit * 2))

    blockers = []
    improvement_actions = []

    if margin < 15:
        blockers.append("Profit margin is below the preferred financing threshold.")
        improvement_actions.append("Improve pricing, reduce direct costs, or focus on higher-margin products.")
    elif margin < 25:
        improvement_actions.append("Raise profit margin toward 25-30% to strengthen financing confidence.")

    if expense_ratio > 0.80:
        blockers.append("Operating expenses consume most of the revenue.")
        improvement_actions.append("Reduce non-critical expenses and review the largest expense categories first.")
    elif expense_ratio > 0.65:
        improvement_actions.append("Improve cost efficiency by controlling recurring operating expenses.")

    if overdue_ratio > 0.20:
        blockers.append("Overdue invoices may pressure cash flow.")
        improvement_actions.append("Improve collections and reduce overdue invoices below 20%.")
    elif overdue_ratio > 0.10:
        improvement_actions.append("Keep improving invoice collection speed to reduce cash-flow risk.")

    if float(health.get("score", 0)) < 70:
        blockers.append("Financial health score is not yet strong enough for a confident review.")
        improvement_actions.append("Improve financial health through profitability, cost control, and collections.")

    if profit <= 0:
        blockers.append("The company is not currently profitable.")
        improvement_actions.append("Reach consistent positive net profit before requesting larger financing limits.")

    if not blockers:
        blockers.append("No major blocker detected from the uploaded financial data.")
    if not improvement_actions:
        improvement_actions.append("Maintain profitability, keep expenses controlled, and monitor collections monthly.")

    return {
        "score": score,
        "grade": grade,
        "risk": risk,
        "recommendation": recommendation,
        "suggested_limit": suggested_limit,
        "factors": factors,
        "blockers": blockers,
        "improvement_actions": improvement_actions,
    }
