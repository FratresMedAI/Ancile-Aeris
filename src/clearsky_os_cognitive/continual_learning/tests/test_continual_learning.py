def update_mode(safety_open: bool) -> str:
    return "observe_only" if not safety_open else "bounded_adaptation_stub"


def test_update_mode_respects_safety() -> None:
    assert update_mode(False) == "observe_only"
    assert update_mode(True) == "bounded_adaptation_stub"
