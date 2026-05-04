from collections import deque


def behavior_from_history(window: deque[dict]) -> str:
    if len(window) < 2:
        return "observe"
    first = window[0]
    last = window[-1]
    dx = float(last.get("x", 0.0)) - float(first.get("x", 0.0))
    dy = float(last.get("y", 0.0)) - float(first.get("y", 0.0))
    distance = (dx * dx + dy * dy) ** 0.5
    if distance < 3.0:
        return "loiter"
    if abs(dx) + abs(dy) > 15.0:
        return "rapid_descent"
    return "approach"


def test_loiter_detection() -> None:
    w = deque([{"x": 10.0, "y": 10.0}, {"x": 11.0, "y": 10.5}], maxlen=20)
    assert behavior_from_history(w) == "loiter"


def test_rapid_descent_detection() -> None:
    w = deque([{"x": 0.0, "y": 0.0}, {"x": 20.0, "y": 3.0}], maxlen=20)
    assert behavior_from_history(w) == "rapid_descent"
