def calculate_financial_health(
    profit_margin,
    expense_ratio,
    overdue_ratio
):
    """
    Calculate a realistic Financial Health Score from 0 to 100.
    """
    score = 0

    # Profitability: max 35 points
    if profit_margin >= 50:
        score += 32
    elif profit_margin >= 30:
        score += 27
    elif profit_margin >= 15:
        score += 20
    elif profit_margin >= 5:
        score += 12
    elif profit_margin >= 0:
        score += 5
    else:
        score += 0

    # Expense efficiency: max 30 points
    if expense_ratio <= 0.35:
        score += 28
    elif expense_ratio <= 0.50:
        score += 24
    elif expense_ratio <= 0.65:
        score += 18
    elif expense_ratio <= 0.80:
        score += 10
    elif expense_ratio <= 1.00:
        score += 5
    else:
        score += 0

    # Collection quality: max 20 points
    if overdue_ratio == 0:
        score += 20
    elif overdue_ratio <= 0.10:
        score += 16
    elif overdue_ratio <= 0.20:
        score += 11
    elif overdue_ratio <= 0.30:
        score += 6
    else:
        score += 2

    # Stability buffer: max 15 points
    if profit_margin >= 30 and expense_ratio <= 0.50:
        score += 14
    elif profit_margin >= 15 and expense_ratio <= 0.65:
        score += 10
    elif profit_margin >= 5:
        score += 6
    else:
        score += 2

    score = max(0, min(100, round(score)))

    if score >= 85:
        status = "Excellent"
    elif score >= 70:
        status = "Good"
    elif score >= 55:
        status = "Needs Attention"
    else:
        status = "Critical"

    return {
        "score": score,
        "status": status
    }
