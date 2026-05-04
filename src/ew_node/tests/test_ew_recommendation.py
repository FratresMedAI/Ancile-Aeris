def test_recommendation_low_threat() -> None:
    score = 0.5
    action = "monitor" if score < 0.7 else "prioritize_tracking_and_deconfliction"
    assert action == "monitor"


def test_recommendation_high_threat() -> None:
    score = 0.9
    action = "monitor" if score < 0.7 else "prioritize_tracking_and_deconfliction"
    assert action == "prioritize_tracking_and_deconfliction"
