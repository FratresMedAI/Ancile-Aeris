def verify_action(pid_score: float, pid_gate: float, human_veto_possible: bool) -> tuple[bool, str]:
    if not human_veto_possible:
        return False, "human_veto_unavailable"
    if pid_score < pid_gate:
        return False, "pid_threshold_not_met"
    return True, "verified"


def test_verify_action_blocks_low_pid() -> None:
    approved, reason = verify_action(0.95, 0.999, True)
    assert not approved
    assert reason == "pid_threshold_not_met"
