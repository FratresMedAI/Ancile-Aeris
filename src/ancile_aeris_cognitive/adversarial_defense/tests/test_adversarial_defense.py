import statistics


def anomaly_score(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return min(1.0, statistics.pstdev(values))


def test_anomaly_score_detects_variance() -> None:
    assert anomaly_score([1.0, 1.0, 1.0]) == 0.0
    assert anomaly_score([0.0, 2.0, 0.0, 2.0]) > 0.3
