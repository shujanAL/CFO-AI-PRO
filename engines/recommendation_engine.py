from utils.i18n import sar, tr


def generate_recommendation(best, metrics, language="en"):
    decision, category, value = best["Decision"], best["Category"], best["Value"]
    profit, change = best["Expected Profit"], best["Profit Change"]
    health, risk, confidence = best["Health"], best["Risk"], best["Confidence"]
    if language == "ar":
        confidence_ar = {"High": "عالية", "Medium": "متوسطة", "Low": "منخفضة"}.get(confidence, confidence)
        if decision == "Increase Sales":
            action = f"تنفيذ تجربة محدودة تستهدف نمو المبيعات بنسبة {value}%"
            assumption = "يفترض النموذج أن 35% من الإيراد الإضافي سيُستخدم لتغطية تكلفة تحقيق النمو."
            validation = "راقب تكلفة اكتساب العميل وهامش الربح والتحويل أسبوعيًا قبل التوسع."
        else:
            action = f"مراجعة خفض مصروفات {tr(category, language)} بنسبة {value}%"
            assumption = f"يفترض النموذج خفض فئة {tr(category, language)} فقط دون بقية المصروفات."
            validation = "تأكد أن الخفض لن يؤثر في القدرة التشغيلية أو تجربة العملاء."
        return f"""
## 🤖 توصية تنفيذية مبنية على الأدلة

### الخطوة المقترحة
**{action}**

هذه **توصية مبنية على سيناريو وليست نتيجة مضمونة**. حصلت على أعلى ترتيب بعد موازنة العائد المتوقع والصحة المالية ومخاطر التنفيذ ودرجة الثقة.

### الأثر التقديري
- الربح المتوقع: **{sar(profit, language)}**
- الزيادة التقديرية في الربح: **{sar(abs(change), language)}**
- الصحة المالية بعد السيناريو: **{tr(health, language)}**
- مخاطر التنفيذ: **{tr(risk, language)}**
- درجة ثقة النموذج: **{confidence_ar}**

### الافتراض المستخدم
{assumption}

### قبل اتخاذ القرار
{validation}

يجب على الإدارة اعتماد القرار فقط بعد التحقق من الافتراضات وفق القدرة التشغيلية وبيانات السوق الحالية.
"""
    if decision == "Increase Sales":
        action = f"Run a controlled pilot targeting {value}% sales growth"
        assumption = "35% of incremental revenue is required to deliver growth."
        validation = "Track acquisition cost, gross margin and conversion weekly before scaling."
    else:
        action = f"Review a {value}% reduction in {category} spending"
        assumption = f"Only the {category} category is reduced."
        validation = "Confirm the saving will not reduce delivery capacity or customer experience."
    return f"""
## 🤖 Evidence-Based Executive Recommendation
### Proposed next step
**{action}**

This is a **scenario recommendation**, not a guaranteed outcome. It balances projected return, financial health, execution risk and confidence.

### Estimated impact
- Projected profit: **{sar(profit)}**
- Estimated profit increase: **{sar(abs(change))}**
- Financial health: **{health}**
- Execution risk: **{risk}**
- Model confidence: **{confidence}**

### Assumption used
{assumption}

### Before committing
{validation}
"""
