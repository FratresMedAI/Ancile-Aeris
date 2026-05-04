def evaluate_action(action_type: str, target_id: str, friendly_x_positions: list[float]) -> tuple[bool, str, float]:
    if action_type == "shoot":
        if target_id in {str(x) for x in friendly_x_positions}:
            return False, "Friendly unit in danger", 1.0
        return True, "No friendly unit in danger", 0.0
    return True, "Action not simulated", 0.0


def test_shoot_blocks_friendly_match() -> None:
    success, reason, impact = evaluate_action("shoot", "42.0", [42.0, 11.0])
    assert not success
    assert reason == "Friendly unit in danger"
    assert impact == 1.0


def test_shoot_allows_non_friendly_target() -> None:
    success, reason, impact = evaluate_action("shoot", "13.0", [42.0, 11.0])
    assert success
    assert reason == "No friendly unit in danger"
    assert impact == 0.0
