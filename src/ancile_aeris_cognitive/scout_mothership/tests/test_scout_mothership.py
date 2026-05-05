def loiter_profile() -> dict:
    return {"altitude_m": 4500.0, "endurance_hr": 24.0, "sensors": ["eo_ir", "rf", "acoustic"]}


def test_loiter_profile() -> None:
    profile = loiter_profile()
    assert profile["altitude_m"] > 1000.0
    assert "eo_ir" in profile["sensors"]
