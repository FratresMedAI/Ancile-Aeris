def threat_score(confidence: float, speed_norm: float, predicted_risk: float) -> float:
    return 0.6 * confidence + 0.25 * speed_norm + 0.15 * predicted_risk


def nl_summary(track_id: str, score: float, action: str, uncertainty_total: float) -> str:
    certainty = max(0.0, 1.0 - uncertainty_total)
    return (
        f"Threat score {score:.2f} for {track_id}. Recommended action: {action}. "
        f"Estimated certainty {certainty:.2f} from multimodal agreement and trajectory context."
    )


def safety_gate_reason(
    *,
    pid_passed: bool,
    pid_conf: float,
    pid_gate: float,
    friendly: bool,
    hostile_confirmed: bool,
    twin_risk: float,
    action: str,
    operator_ack: bool,
) -> str:
    if not pid_passed or pid_conf < pid_gate:
        return "blocked_pid_gate"
    if friendly:
        return "blocked_friendly_iff"
    if not hostile_confirmed:
        return "blocked_unconfirmed_hostile_identity"
    if action != "monitor" and twin_risk > 0.0:
        return "blocked_digital_twin_risk"
    if action != "monitor" and not operator_ack:
        return "blocked_no_operator_authorization"
    return "authorized"


def test_threat_score_range() -> None:
    score = threat_score(0.9, 0.5, 0.6)
    assert 0.0 <= score <= 1.0
    assert score > 0.7


def test_low_threat_score() -> None:
    score = threat_score(0.2, 0.1, 0.4)
    assert score < 0.4


def test_pid_gate_blocks() -> None:
    reason = safety_gate_reason(
        pid_passed=False,
        pid_conf=0.95,
        pid_gate=0.999,
        friendly=False,
        hostile_confirmed=True,
        twin_risk=0.0,
        action="jam",
        operator_ack=True,
    )
    assert reason == "blocked_pid_gate"


def test_friendly_veto_blocks() -> None:
    reason = safety_gate_reason(
        pid_passed=True,
        pid_conf=0.999,
        pid_gate=0.999,
        friendly=True,
        hostile_confirmed=True,
        twin_risk=0.0,
        action="jam",
        operator_ack=True,
    )
    assert reason == "blocked_friendly_iff"


def test_twin_risk_veto_blocks() -> None:
    reason = safety_gate_reason(
        pid_passed=True,
        pid_conf=0.999,
        pid_gate=0.999,
        friendly=False,
        hostile_confirmed=True,
        twin_risk=0.2,
        action="jam",
        operator_ack=True,
    )
    assert reason == "blocked_digital_twin_risk"


def test_operator_ack_required() -> None:
    reason = safety_gate_reason(
        pid_passed=True,
        pid_conf=0.999,
        pid_gate=0.999,
        friendly=False,
        hostile_confirmed=True,
        twin_risk=0.0,
        action="jam",
        operator_ack=False,
    )
    assert reason == "blocked_no_operator_authorization"


def test_nl_summary_contains_action_and_certainty() -> None:
    text = nl_summary("trk-1", 0.87, "monitor", 0.22)
    assert "trk-1" in text
    assert "monitor" in text
    assert "0.78" in text
