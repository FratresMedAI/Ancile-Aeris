def choose_action(confidence: float) -> str:
    if confidence > 0.8:
        return "spoof"
    if confidence > 0.6:
        return "jam"
    return "monitor"


def test_choose_high_confidence() -> None:
    assert choose_action(0.9) == "spoof"


def test_choose_mid_confidence() -> None:
    assert choose_action(0.7) == "jam"
