def generate_executive_summary(metrics, forecast):

    summary = []

    summary.append(
        f"Financial Health: {metrics['financial_status']}"
    )

    summary.append(
        f"Total Revenue: {metrics['total_sales']:,.0f} SAR"
    )

    summary.append(
        f"Net Profit: {metrics['net_profit']:,.0f} SAR"
    )

    summary.append(
        f"Profit Margin: {metrics['profit_margin']:.1f}%"
    )

    if forecast.iloc[-1]["Forecasted Sales"] > forecast.iloc[0]["Forecasted Sales"]:
        summary.append(
            "Forecast indicates positive revenue growth."
        )
    else:
        summary.append(
            "Forecast indicates stable revenue."
        )

    return summary