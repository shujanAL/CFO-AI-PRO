import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_monthly_sales(sales_df, months_ahead=3):
    df = sales_df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    monthly = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
        .reset_index()
    )

    monthly["Date"] = monthly["Date"].dt.to_timestamp()
    monthly["month_index"] = range(len(monthly))

    if monthly.empty:
        return pd.DataFrame(columns=["Date", "Forecasted Sales"])

    if len(monthly) == 1:
        last_date = monthly["Date"].iloc[0]
        amount = max(0, float(monthly["Amount"].iloc[0]))
        return pd.DataFrame({
            "Date": [last_date + pd.DateOffset(months=i) for i in range(1, months_ahead + 1)],
            "Forecasted Sales": [amount] * months_ahead,
        })

    X = monthly[["month_index"]]
    y = monthly["Amount"]

    model = LinearRegression()
    model.fit(X, y)

    future_rows = []

    last_date = monthly["Date"].max()
    last_index = monthly["month_index"].max()

    for i in range(1, months_ahead + 1):
        future_index = last_index + i
        future_date = last_date + pd.DateOffset(months=i)

        predicted_amount = max(0, model.predict([[future_index]])[0])

        future_rows.append({
            "Date": future_date,
            "Forecasted Sales": round(predicted_amount, 2)
        })

    return pd.DataFrame(future_rows)
