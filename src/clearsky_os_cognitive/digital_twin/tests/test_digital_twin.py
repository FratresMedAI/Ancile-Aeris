from digital_twin.physics import evaluate_proposal
from digital_twin.rollout import evaluate_rollout


def test_evaluate_proposal_bounds() -> None:
    result = evaluate_proposal(
        track_x=30.0,
        track_y=0.0,
        track_vx=-10.0,
        track_vy=0.0,
        threat_score=0.8,
        mitigation_gain=0.7,
        asset_radius_m=25.0,
        safety_open=True,
    )
    assert 0.0 <= result.effectiveness_probability <= 1.0
    assert 0.0 <= result.collateral_risk_score <= 1.0
    assert 0.0 <= result.risk <= 1.0


def test_high_proximity_can_veto() -> None:
    result = evaluate_proposal(
        track_x=5.0,
        track_y=0.0,
        track_vx=-20.0,
        track_vy=0.0,
        threat_score=0.95,
        mitigation_gain=0.2,
        asset_radius_m=25.0,
        risk_veto_threshold=0.5,
        safety_open=False,
    )
    assert result.risk >= 0.5
    assert result.veto is True


def test_far_slow_track_low_risk() -> None:
    result = evaluate_proposal(
        track_x=200.0,
        track_y=200.0,
        track_vx=1.0,
        track_vy=0.0,
        threat_score=0.3,
        mitigation_gain=0.8,
        asset_radius_m=25.0,
        risk_veto_threshold=0.65,
        safety_open=True,
    )
    assert result.risk < 0.65
    assert result.veto is False


def test_rollout_raises_risk_for_inbound() -> None:
    now = evaluate_proposal(
        track_x=120.0,
        track_y=0.0,
        track_vx=-30.0,
        track_vy=0.0,
        threat_score=0.8,
        mitigation_gain=0.3,
        asset_radius_m=25.0,
        risk_veto_threshold=0.65,
        safety_open=False,
    )
    rolled = evaluate_rollout(
        track_x=120.0,
        track_y=0.0,
        track_vx=-30.0,
        track_vy=0.0,
        threat_score=0.8,
        mitigation_gain=0.3,
        safety_open=False,
    )
    assert rolled.risk >= now.risk
    assert "gazebo_rollout" in rolled.rationale
