from utils.i18n import sar, tr


def _number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _best_expense_to_reduce(context):
    for decision in context.get("top_decisions", []):
        if str(decision.get("Decision", "")).lower().startswith("reduce"):
            return decision
    return None


def _forecast_direction(context):
    forecast = context.get("forecast", [])
    if len(forecast) < 2:
        return "stable"
    first = _number(forecast[0].get("Forecasted Sales"))
    last = _number(forecast[-1].get("Forecasted Sales"))
    if last > first:
        return "up"
    if last < first:
        return "down"
    return "stable"


def ask_rule_based_copilot(question, context, language="en"):
    q = question.lower()
    metrics = context.get("metrics", {})
    health = context.get("health", {})
    financing = context.get("financing", {})
    best = context.get("best_decision", {})

    profit_margin = _number(metrics.get("profit_margin"))
    expense_ratio = _number(metrics.get("expense_ratio"))
    overdue_ratio = _number(metrics.get("overdue_ratio"))
    net_profit = _number(metrics.get("net_profit"))
    health_score = _number(health.get("score"))
    health_status = health.get("status", "Unknown")
    readiness_score = _number(financing.get("score"))
    readiness_grade = financing.get("grade", "N/A")
    forecast_direction = _forecast_direction(context)
    best_expense = _best_expense_to_reduce(context)

    if language == "ar":
        intro = "اعتمادًا على البيانات والتحليلات الحالية فقط:"
        if "health" in q or "صحة" in q or "ليش" in q or "why" in q:
            return f"""{intro}

درجة الصحة المالية هي {health_score:.0f}/100 وتصنيفها {tr(health_status, language)}.
أهم العوامل المؤثرة: هامش الربح {profit_margin:.1f}%، نسبة المصروفات {expense_ratio:.1%}، ونسبة الفواتير المتأخرة {overdue_ratio:.1%}.
إذا أردت رفع الدرجة، ابدأ بتحسين هامش الربح وتقليل المصروفات ذات الأثر الأعلى ومتابعة التحصيل."""

        if "risk" in q or "خطر" in q or "مخاطر" in q:
            risks = []
            if expense_ratio > 0.8:
                risks.append("المصروفات تستهلك نسبة عالية من الإيرادات")
            if overdue_ratio > 0.2:
                risks.append("الفواتير المتأخرة قد تضغط على التدفق النقدي")
            if profit_margin < 15:
                risks.append("هامش الربح منخفض")
            if not risks:
                risks.append("المخاطر الحالية تبدو تحت السيطرة، لكن يلزم متابعة المصروفات والتحصيل")
            return intro + "\n\nأكبر المخاطر: " + "، ".join(risks) + "."

        if "financ" in q or "loan" in q or "تمويل" in q or "بنك" in q:
            return f"""{intro}

جاهزية التمويل الحالية {readiness_score:.0f}/100 بدرجة {readiness_grade}.
إذا كانت الدرجة مرتفعة فهذا يدعم التقديم للمراجعة البنكية، لكن القرار النهائي يحتاج مستندات ومراجعة بشرية.
قبل التقديم، ركّز على تقليل الفواتير المتأخرة وتحسين الربحية لأنها تؤثر مباشرة على الثقة الائتمانية."""

        if "hire" in q or "employee" in q or "موظف" in q or "توظيف" in q:
            if profit_margin >= 25 and health_score >= 75:
                advice = "يمكن دراسة التوظيف بشكل تدريجي، بشرط أن يكون مرتبطًا بزيادة واضحة في المبيعات أو الإنتاجية."
            else:
                advice = "لا أنصح بالتوظيف الكبير الآن؛ الأفضل اختبار موظف أو عقد مؤقت حتى تتحسن الربحية والصحة المالية."
            return f"{intro}\n\n{advice}\nصافي الربح الحالي {sar(net_profit, language)} وهامش الربح {profit_margin:.1f}%."

        if "expense" in q or "reduce" in q or "مصروف" in q or "أخفض" in q:
            if best_expense:
                category = tr(best_expense.get("Category", "Expenses"), language)
                value = best_expense.get("Value", 0)
                impact = sar(best_expense.get("Expected Profit", 0), language)
                return f"{intro}\n\nابدأ بمراجعة مصروفات {category} بنسبة تقريبية {value}%. هذا السيناريو من أعلى الخيارات في الترتيب، والربح المتوقع بعده {impact}."
            return f"{intro}\n\nابدأ بالمصروفات الأكبر والأقل تأثيرًا على التشغيل، وراقب ألا يؤثر الخفض على جودة الخدمة أو المبيعات."

        action = tr(best.get("Decision", "Review current plan"), language)
        trend = "صاعد" if forecast_direction == "up" else "هابط" if forecast_direction == "down" else "مستقر"
        return f"""{intro}

أفضل اتجاه حاليًا حسب ترتيب القرارات هو: {action}.
الصحة المالية {health_score:.0f}/100، هامش الربح {profit_margin:.1f}%، واتجاه التوقعات {trend}.
نصيحتي: نفّذ القرار كتجربة محدودة ثم راقب الربح والتحصيل قبل التوسع."""

    if "health" in q or "why" in q:
        return f"""Based only on the current analysis:

Financial Health is {health_score:.0f}/100 ({health_status}).
The main drivers are profit margin ({profit_margin:.1f}%), expense ratio ({expense_ratio:.1%}), and overdue invoices ({overdue_ratio:.1%}).
To improve the score, focus on margin, high-impact expenses, and collections."""

    if "risk" in q:
        risks = []
        if expense_ratio > 0.8:
            risks.append("operating expenses consume a high share of revenue")
        if overdue_ratio > 0.2:
            risks.append("overdue invoices may pressure cash flow")
        if profit_margin < 15:
            risks.append("profit margin is weak")
        if not risks:
            risks.append("current risk looks controlled, but expenses and collections should still be monitored")
        return "Based only on the current analysis, the biggest risk is: " + "; ".join(risks) + "."

    if "financ" in q or "loan" in q or "bank" in q:
        return f"""Based only on the current analysis:

Financing readiness is {readiness_score:.0f}/100 with grade {readiness_grade}.
This can support a bank review, but it is not an automated credit decision. Before applying, improve overdue collections and profitability because both affect lender confidence."""

    if "hire" in q or "employee" in q:
        if profit_margin >= 25 and health_score >= 75:
            advice = "Hiring can be tested gradually if each role is tied to measurable sales growth or productivity."
        else:
            advice = "Avoid major hiring right now; test one role or a temporary contract until profitability and health improve."
        return f"Based only on the current analysis:\n\n{advice}\nCurrent net profit is {sar(net_profit)} and profit margin is {profit_margin:.1f}%."

    if "expense" in q or "reduce" in q or "cost" in q:
        if best_expense:
            category = best_expense.get("Category", "Expenses")
            value = best_expense.get("Value", 0)
            impact = sar(best_expense.get("Expected Profit", 0))
            return f"Based only on the current analysis:\n\nStart by reviewing {category} spending by about {value}%. It appears in the top ranked scenarios, with projected profit after the scenario of {impact}."
        return "Based only on the current analysis:\n\nStart with the largest controllable expense that has the lowest operational impact, while protecting service quality and sales capacity."

    action = best.get("Decision", "Review the current plan")
    return f"""Based only on the current analysis:

The strongest current direction is: {action}.
Financial Health is {health_score:.0f}/100, profit margin is {profit_margin:.1f}%, and the forecast trend is {forecast_direction}.
My advice: run it as a limited pilot, then monitor profit and collections before scaling."""
