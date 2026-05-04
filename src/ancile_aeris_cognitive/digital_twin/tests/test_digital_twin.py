def score_effectiveness(threat_score: float, mitigation_gain: float) -> tuple[float, float]:
    effectiveness = min(1.0, max(0.0, 0.5 * threat_score + 0.5 * mitigation_gain))
    collateral = max(0.0, 1.0 - effectiveness)
    return effectiveness, collateral


def test_score_effectiveness_bounds() -> None:
    effectiveness, collateral = score_effectiveness(0.8, 0.7)
    assert 0.0 <= effectiveness <= 1.0
    assert 0.0 <= collateral <= 1.0
