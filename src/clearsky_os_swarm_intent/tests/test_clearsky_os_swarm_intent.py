def classify_swarm(tracks: list[dict]) -> str:
    if len(tracks) >= 6:
        return "saturation_attack"
    if len(tracks) >= 3:
        return "probe_cluster"
    return "single_or_scatter"


def test_saturation_classification() -> None:
    assert classify_swarm([{}] * 6) == "saturation_attack"


def test_probe_cluster_classification() -> None:
    assert classify_swarm([{}] * 4) == "probe_cluster"


def test_single_classification() -> None:
    assert classify_swarm([{}]) == "single_or_scatter"
