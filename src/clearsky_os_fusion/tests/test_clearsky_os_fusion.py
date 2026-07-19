def confidence_vote(visual: float, acoustic: float, rf: float, lidar: float, sigint: float) -> float:
    return (0.35 * visual) + (0.2 * acoustic) + (0.2 * rf) + (0.15 * lidar) + (0.1 * sigint)


def test_confidence_vote_weighting() -> None:
    out = confidence_vote(0.9, 0.5, 0.5, 0.2, 0.2)
    assert out > 0.55


def test_confidence_vote_bounds() -> None:
    out = confidence_vote(0.0, 0.0, 0.0, 0.0, 0.0)
    assert out == 0.0
