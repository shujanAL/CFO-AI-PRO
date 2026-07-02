from utils.i18n import sar, tr


def generate_simulation_analysis(scenario_type, action, result, previous_profit, language="en"):
    difference = result["new_profit"] - previous_profit
    if language == "ar":
        if difference > 0:
            impact = f"من المتوقع ارتفاع الربح بمقدار {sar(difference, language)}."
        elif difference < 0:
            impact = f"من المتوقع انخفاض الربح بمقدار {sar(abs(difference), language)}."
        else:
            impact = "لا يوجد تغير جوهري في الربح."
        return f"""
## 🤖 تحليل المحاكاة
**الإجراء:** {tr(action, language)}  
**نوع القرار:** {tr(scenario_type, language)}  
**أثر القرار:** {impact}  
**الصحة المالية بعد المحاكاة:** {tr(result['new_health_status'], language)}

هذا التحليل مبني على افتراضات السيناريو المحدد فقط.
"""
    if difference > 0:
        impact = f"Profit is expected to increase by {sar(difference)}."
    elif difference < 0:
        impact = f"Profit is expected to decrease by {sar(abs(difference))}."
    else:
        impact = "No significant change in profit."
    return f"""
## 🤖 AI Simulation Analysis
**Action:** {action}  
**Decision type:** {scenario_type}  
**Business impact:** {impact}  
**Financial health:** {result['new_health_status']}

This analysis is based on the selected simulation only.
"""
