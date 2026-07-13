AR_FINANCING_TEXT = {
    "No major blocker detected from the uploaded financial data.": "لا توجد عوائق تمويلية رئيسية ظاهرة من البيانات المرفوعة.",
    "Keep improving invoice collection speed to reduce cash-flow risk.": "استمر في تحسين سرعة تحصيل الفواتير لتقليل مخاطر التدفق النقدي.",
    "Profit margin is below the preferred financing threshold.": "هامش الربح أقل من المستوى المفضل للتمويل.",
    "Improve pricing, reduce direct costs, or focus on higher-margin products.": "حسّن التسعير، أو خفّض التكاليف المباشرة، أو ركّز على المنتجات الأعلى ربحية.",
    "Raise profit margin toward 25-30% to strengthen financing confidence.": "ارفع هامش الربح باتجاه 25-30% لتعزيز ثقة جهة التمويل.",
    "Operating expenses consume most of the revenue.": "المصروفات التشغيلية تستهلك معظم الإيرادات.",
    "Reduce non-critical expenses and review the largest expense categories first.": "خفّض المصروفات غير الأساسية وراجع أكبر فئات المصروفات أولاً.",
    "Improve cost efficiency by controlling recurring operating expenses.": "حسّن كفاءة التكاليف عبر ضبط المصروفات التشغيلية المتكررة.",
    "Overdue invoices may pressure cash flow.": "الفواتير المتأخرة قد تضغط على التدفق النقدي.",
    "Improve collections and reduce overdue invoices below 20%.": "حسّن التحصيل وخفّض الفواتير المتأخرة إلى أقل من 20%.",
    "Financial health score is not yet strong enough for a confident review.": "درجة الصحة المالية ليست قوية بما يكفي لمراجعة تمويلية واثقة.",
    "Improve financial health through profitability, cost control, and collections.": "حسّن الصحة المالية عبر الربحية، وضبط التكاليف، والتحصيل.",
    "The company is not currently profitable.": "الشركة ليست رابحة حاليًا.",
    "Reach consistent positive net profit before requesting larger financing limits.": "حقق صافي ربح إيجابي ومستقر قبل طلب حدود تمويلية أكبر.",
}

AR_TREND_TEXT = {
    "Growing": "صاعد",
    "Declining": "هابط",
    "Stable": "مستقر",
}


def finance_text(value, language="en"):
    if language != "ar":
        return value
    return AR_FINANCING_TEXT.get(str(value), value)


def trend_text(value, language="en"):
    if language != "ar":
        return value
    return AR_TREND_TEXT.get(str(value), value)
