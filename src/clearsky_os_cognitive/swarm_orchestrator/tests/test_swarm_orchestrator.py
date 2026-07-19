def cluster_size_to_intent(cluster_size: int) -> str:
    if cluster_size >= 6:
        return "coordinated_swarm"
    if cluster_size >= 3:
        return "probing_group"
    return "single_actor"


def test_cluster_size_to_intent() -> None:
    assert cluster_size_to_intent(1) == "single_actor"
    assert cluster_size_to_intent(4) == "probing_group"
    assert cluster_size_to_intent(8) == "coordinated_swarm"
