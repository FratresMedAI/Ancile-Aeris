def confidence_vote(visual: float, acoustic: float, rf: float) -> float:
    return 0.5 * visual + 0.25 * acoustic + 0.25 * rf


def pid_passed(confidence: float, modalities: set[str], gate: float = 0.999) -> bool:
    required = {"visual", "acoustic", "rf"}
    return required.issubset(modalities) and confidence >= gate


def test_confidence_vote_bounds() -> None:
    value = confidence_vote(0.9, 0.8, 0.7)
    assert 0.0 <= value <= 1.0
    assert value > 0.8


def test_confidence_vote_low_signal() -> None:
    value = confidence_vote(0.1, 0.2, 0.1)
    assert value < 0.2


def test_pid_requires_all_required_modalities() -> None:
    assert not pid_passed(1.0, {"visual", "rf"}, gate=0.999)


def test_pid_requires_gate_threshold() -> None:
    assert not pid_passed(0.995, {"visual", "acoustic", "rf"}, gate=0.999)


def test_pid_passes_only_with_required_inputs_and_threshold() -> None:
    assert pid_passed(0.999, {"visual", "acoustic", "rf", "lidar"}, gate=0.999)
