def generate_ai_summary(metrics, language="en"):
    ar = language == "ar"
    summary = []
    if metrics["profit_margin"] >= 30:
        summary.append("✅ تتمتع الشركة بهامش ربح ممتاز." if ar else "✅ The company has an excellent profit margin.")
    elif metrics["profit_margin"] >= 15:
        summary.append("🟡 هامش الربح مقبول ويمكن تحسينه." if ar else "🟡 Profit margin is acceptable but can be improved.")
    else:
        summary.append("🔴 هامش الربح منخفض ويحتاج إلى اهتمام." if ar else "🔴 Profit margin is low and requires attention.")
    if metrics["expense_ratio"] > 0.80:
        summary.append("⚠️ تستهلك المصروفات التشغيلية معظم الإيرادات." if ar else "⚠️ Operating expenses are consuming most of the revenue.")
    if metrics["overdue_ratio"] > 0.20:
        summary.append("⚠️ نسبة مرتفعة من الفواتير متأخرة السداد." if ar else "⚠️ A high percentage of invoices are overdue.")
    else:
        summary.append("✅ أداء تحصيل الفواتير جيد." if ar else "✅ Invoice collection performance is healthy.")
    summary.append(
        ("📈 الشركة تحقق أرباحًا حاليًا." if ar else "📈 The company is currently profitable.")
        if metrics["net_profit"] > 0 else
        ("📉 الشركة تعمل بخسارة حاليًا." if ar else "📉 The company is operating at a loss.")
    )
    return summary
