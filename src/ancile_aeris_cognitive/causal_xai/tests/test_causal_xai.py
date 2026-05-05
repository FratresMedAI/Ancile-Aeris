def counterfactual_summary(delay_seconds: float) -> str:
    return f"If action occurred {delay_seconds:.1f}s earlier, projected risk would be reduced in this stub model."


def test_counterfactual_summary_contains_time() -> None:
    assert "8.0s" in counterfactual_summary(8.0)
