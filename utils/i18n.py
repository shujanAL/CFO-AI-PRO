AR = {
    "Excellent": "ممتاز", "Good": "جيد", "Needs Attention": "يحتاج اهتمامًا", "Critical": "حرج",
    "Low": "منخفض", "Moderate": "متوسط", "Elevated": "مرتفع", "High": "عالٍ",
    "Ready for financing review": "جاهز لمراجعة طلب التمويل",
    "Conditionally ready": "جاهز بشروط", "Needs additional review": "يحتاج مراجعة إضافية", "Not ready yet": "غير جاهز حاليًا",
    "Revenue": "الإيرادات", "Expenses": "المصروفات", "Employees": "الموظفون",
    "Increase Sales": "زيادة المبيعات", "Decrease Sales": "خفض المبيعات",
    "Increase Expense": "زيادة المصروف", "Reduce Expense": "خفض المصروف",
    "Hire Employee": "توظيف موظف", "Lay Off Employee": "الاستغناء عن موظف",
    "Salaries": "الرواتب", "Marketing": "التسويق", "Inventory": "المخزون",
    "Rent": "الإيجار", "Utilities": "الخدمات", "Software": "البرمجيات",
    "Sales": "المبيعات", "Finance": "المالية", "Operations": "العمليات", "Support": "الدعم",
    "Data Analyst": "محلل بيانات", "Accountant": "محاسب", "Sales Representative": "مندوب مبيعات",
    "Marketing Specialist": "أخصائي تسويق", "Operations Coordinator": "منسق عمليات", "Customer Support": "دعم العملاء",
    "High": "عالٍ", "Medium": "متوسطة", "Stable": "مستقر", "Positive Outlook": "توقعات إيجابية",
    "Profitability": "الربحية", "Cost efficiency": "كفاءة التكاليف", "Collections": "التحصيل",
    "Financial stability": "الاستقرار المالي", "Revenue": "الإيرادات",
}


def tr(value, language="en"):
    if language != "ar":
        return value
    return AR.get(str(value), value)


def sar(value, language="en"):
    unit = "ر.س" if language == "ar" else "SAR"
    return f"{value:,.0f} {unit}"
