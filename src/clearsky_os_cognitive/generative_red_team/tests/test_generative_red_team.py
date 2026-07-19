def sample_domain_values() -> set[str]:
    return {"swarm_probe", "rf_spoofing", "sensor_blinding", "coordinated_intrusion"}


def test_domain_values_non_empty() -> None:
    assert "swarm_probe" in sample_domain_values()
