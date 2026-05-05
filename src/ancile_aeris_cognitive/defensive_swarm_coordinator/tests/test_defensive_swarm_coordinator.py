def formation_mode(threat_level: str) -> str:
    return "containment_screen" if threat_level in {"high", "critical"} else "monitor_perimeter"


def test_formation_mode() -> None:
    assert formation_mode("high") == "containment_screen"
    assert formation_mode("low") == "monitor_perimeter"
