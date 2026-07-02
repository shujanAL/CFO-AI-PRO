from engines.financing_readiness import calculate_financing_readiness


def test_financing_readiness_is_bounded_and_explainable():
    metrics = {
        "profit_margin": 25,
        "expense_ratio": 0.60,
        "overdue_ratio": 0.10,
        "net_profit": 250_000,
        "total_sales": 1_000_000,
    }
    result = calculate_financing_readiness(metrics, {"score": 75})

    assert 0 <= result["score"] <= 100
    assert result["grade"] in {"A", "B", "C", "D"}
    assert len(result["factors"]) == 4
    assert result["suggested_limit"] == 200_000
