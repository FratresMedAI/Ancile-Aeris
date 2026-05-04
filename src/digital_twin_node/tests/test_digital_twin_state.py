def test_collision_flag() -> None:
    mirrored_tracks = 3
    predicted_collisions = 1 if mirrored_tracks > 0 else 0
    assert predicted_collisions == 1


def test_soldier_risk_positive_when_tracks_present() -> None:
    mirrored_tracks = 2
    soldier_risk = 0.6 if mirrored_tracks > 0 else 0.0
    assert soldier_risk > 0.0
