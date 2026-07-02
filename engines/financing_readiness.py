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

    return {
        "score": score,
        "grade": grade,
        "risk": risk,
        "recommendation": recommendation,
        "suggested_limit": suggested_limit,
        "factors": factors,
    }
