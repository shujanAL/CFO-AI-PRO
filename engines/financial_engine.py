import pandas as pd
import numpy as np


def calculate_financial_health(total_sales, total_expenses, net_profit, profit_margin, overdue_ratio):
    score = 100

    if profit_margin < 0:
        score -= 35
    elif profit_margin < 5:
        score -= 25
    elif profit_margin < 15:
        score -= 10

    expense_ratio = total_expenses / total_sales if total_sales > 0 else 1

    if expense_ratio > 1:
        score -= 30
    elif expense_ratio > 0.85:
        score -= 20
    elif expense_ratio > 0.70:
        score -= 10

    if overdue_ratio > 0.25:
        score -= 20
    elif overdue_ratio > 0.15:
        score -= 10

    score = max(0, min(100, round(score)))

    if score >= 80:
        status = "Excellent"
    elif score >= 60:
        status = "Good"
    elif score >= 40:
        status = "Warning"
    else:
        status = "Critical"

    return score, status


def detect_expense_anomalies(expenses_df):
    df = expenses_df.copy()

    if df.empty:
        return pd.DataFrame()

    df["z_score"] = df.groupby("category")["amount"].transform(
        lambda x: (x - x.mean()) / x.std() if x.std() != 0 else 0
    )

    anomalies = df[df["z_score"] > 2.5].copy()
    anomalies = anomalies.sort_values("amount", ascending=False)

    return anomalies[["expense_date", "category", "amount", "description", "z_score"]].head(10)


def generate_recommendations(total_sales, total_expenses, net_profit, profit_margin, overdue_count, top_expense_category):
    recommendations = []

    if net_profit < 0:
        recommendations.append(
            "الشركة تحقق خسارة حالياً. الأولوية هي خفض المصروفات التشغيلية ومراجعة أكبر بنود الإنفاق."
        )

    if profit_margin < 10:
        recommendations.append(
            "هامش الربح منخفض. يُنصح بمراجعة التسعير، تكلفة المنتجات، والمصاريف المتكررة."
        )

    if overdue_count > 0:
        recommendations.append(
            f"يوجد {overdue_count} فاتورة متأخرة. تحسين تحصيل الفواتير قد يرفع السيولة بشكل مباشر."
        )

    if top_expense_category:
        recommendations.append(
            f"أكبر بند مصروفات هو {top_expense_category}. يفضل مراجعته لأنه الأكثر تأثيراً على الربحية."
        )

    if not recommendations:
        recommendations.append(
            "الوضع المالي مستقر. يمكن التركيز على التوسع مع المحافظة على الاحتياطي النقدي."
        )

    return recommendations


def generate_ai_summary(total_sales, total_expenses, net_profit, profit_margin, health_score, health_status):
    return f"""
    بناءً على البيانات الحالية، بلغت المبيعات {total_sales:,.0f} ريال، بينما بلغت المصروفات {total_expenses:,.0f} ريال.
    صافي الربح هو {net_profit:,.0f} ريال، وهامش الربح {profit_margin:.1f}%.
    درجة الصحة المالية الحالية هي {health_score}/100، وتصنيف الوضع المالي هو {health_status}.
    """