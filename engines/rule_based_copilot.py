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


def _has(text, keywords):
    return any(keyword in text for keyword in keywords)


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
        if _has(q, ["توقع", "forecast", "مبيعات جاية", "الشهور", "sales forecast"]):
            trend = "صاعد" if forecast_direction == "up" else "هابط" if forecast_direction == "down" else "مستقر"
            return f"""{intro}

اتجاه توقعات المبيعات يبدو {trend}.
إذا كان الاتجاه صاعدًا، الأفضل دعم النمو بدون رفع المصروفات بسرعة. وإذا كان هابطًا، راجع أسباب انخفاض المبيعات وركّز على التحصيل وخفض المصروفات المرنة.
هذه قراءة مبنية على بيانات المبيعات الحالية وليست ضمانًا للنتائج القادمة."""

        if _has(q, ["health", "صحة", "ليش", "why", "درجة", "score"]):
            return f"""{intro}

درجة الصحة المالية هي {health_score:.0f}/100 وتصنيفها {tr(health_status, language)}.
أهم العوامل المؤثرة: هامش الربح {profit_margin:.1f}%، نسبة المصروفات {expense_ratio:.1%}، ونسبة الفواتير المتأخرة {overdue_ratio:.1%}.
إذا أردت رفع الدرجة، ابدأ بتحسين هامش الربح وتقليل المصروفات ذات الأثر الأعلى ومتابعة التحصيل."""

        if _has(q, ["risk", "خطر", "مخاطر", "مشكلة", "ضعف"]):
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

        if _has(q, ["financ", "loan", "تمويل", "بنك", "قرض", "ائتمان"]):
            return f"""{intro}

جاهزية التمويل الحالية {readiness_score:.0f}/100 بدرجة {readiness_grade}.
إذا كانت الدرجة مرتفعة فهذا يدعم التقديم للمراجعة البنكية، لكن القرار النهائي يحتاج مستندات ومراجعة بشرية.
قبل التقديم، ركّز على تقليل الفواتير المتأخرة وتحسين الربحية لأنها تؤثر مباشرة على الثقة الائتمانية."""

        if _has(q, ["hire", "employee", "موظف", "موظفين", "توظيف", "أوظف", "اوظف"]):
            if profit_margin >= 25 and health_score >= 75:
                advice = "يمكن دراسة التوظيف بشكل تدريجي، بشرط أن يكون مرتبطًا بزيادة واضحة في المبيعات أو الإنتاجية."
            else:
                advice = "لا أنصح بالتوظيف الكبير الآن؛ الأفضل اختبار موظف أو عقد مؤقت حتى تتحسن الربحية والصحة المالية."
            return f"{intro}\n\n{advice}\nصافي الربح الحالي {sar(net_profit, language)} وهامش الربح {profit_margin:.1f}%."

        if _has(q, ["expense", "reduce", "cost", "مصروف", "مصروفات", "أخفض", "اخفض", "تكلفة", "تكاليف"]):
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

    if _has(q, ["forecast", "sales forecast", "future sales", "next months", "trend"]):
        return f"""Based only on the current analysis:

The sales forecast trend looks {forecast_direction}.
If the trend is up, support growth without increasing fixed costs too quickly. If it is down, review sales drivers, collections, and flexible expenses.
This is a projection from current sales data, not a guaranteed outcome."""

    if _has(q, ["health", "why", "score"]):
        return f"""Based only on the current analysis:

Financial Health is {health_score:.0f}/100 ({health_status}).
The main drivers are profit margin ({profit_margin:.1f}%), expense ratio ({expense_ratio:.1%}), and overdue invoices ({overdue_ratio:.1%}).
To improve the score, focus on margin, high-impact expenses, and collections."""

    if _has(q, ["risk", "problem", "weakness", "danger"]):
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

    if _has(q, ["financ", "loan", "bank", "credit"]):
        return f"""Based only on the current analysis:

Financing readiness is {readiness_score:.0f}/100 with grade {readiness_grade}.
This can support a bank review, but it is not an automated credit decision. Before applying, improve overdue collections and profitability because both affect lender confidence."""

    if _has(q, ["hire", "employee", "employees", "recruit"]):
        if profit_margin >= 25 and health_score >= 75:
            advice = "Hiring can be tested gradually if each role is tied to measurable sales growth or productivity."
        else:
            advice = "Avoid major hiring right now; test one role or a temporary contract until profitability and health improve."
        return f"Based only on the current analysis:\n\n{advice}\nCurrent net profit is {sar(net_profit)} and profit margin is {profit_margin:.1f}%."

    if _has(q, ["expense", "reduce", "cost", "spending", "cut"]):
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
