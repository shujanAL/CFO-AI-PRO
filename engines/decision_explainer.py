def explain_decision(
    scenario_type,
    action,
    category,
    percentage,
    before,
    after
):

    change = after - before

    if scenario_type == "Expenses":

        if action == "Increase Expense":

            return (
                f"{category} expenses increased by "
                f"{change:,.0f} SAR "
                f"({percentage}%). "
                f"This reduced the company's profit."
            )

        else:

            return (
                f"{category} expenses decreased by "
                f"{abs(change):,.0f} SAR "
                f"({percentage}%). "
                f"This improved the company's profitability."
            )

    elif scenario_type == "Revenue":

        if action == "Increase Sales":

            return (
                f"Sales increased by "
                f"{change:,.0f} SAR. "
                f"The company's profitability improved."
            )

        else:

            return (
                f"Sales decreased by "
                f"{abs(change):,.0f} SAR. "
                f"The company's profitability declined."
            )

    elif scenario_type == "Employees":

        if action == "Hire Employee":

            return (
                "Hiring additional employees increased operating costs "
                "but may improve future business performance."
            )

        else:

            return (
                "Reducing employees lowered operating costs "
                "but may affect business capacity."
            )