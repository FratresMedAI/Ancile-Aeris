def classify_behavior(speed: float, turn_rate: float) -> str:
    if speed < 2.0:
        return "loiter"
    if turn_rate > 0.7:
        return "evasive"
    return "approach"


def test_classify_behavior() -> None:
    assert classify_behavior(1.0, 0.1) == "loiter"
    assert classify_behavior(8.0, 0.9) == "evasive"
