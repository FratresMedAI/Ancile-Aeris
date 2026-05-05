def integrity_state(gps_health: float) -> str:
    if gps_health < 0.3:
        return "denied_fallback_inertial"
    if gps_health < 0.6:
        return "degraded_blended"
    return "nominal_gnss"


def test_integrity_state() -> None:
    assert integrity_state(0.2) == "denied_fallback_inertial"
    assert integrity_state(0.8) == "nominal_gnss"
