def derive_rf_parameters(score: float) -> dict:
    return {
        "center_frequency_hz": 2_450_000_000.0,
        "bandwidth_hz": 20_000_000.0 + (5_000_000.0 * score),
        "power_dbm": -5.0 + (10.0 * score),
    }


def test_derive_rf_parameters_scaling() -> None:
    low = derive_rf_parameters(0.1)
    high = derive_rf_parameters(0.9)
    assert high["bandwidth_hz"] > low["bandwidth_hz"]
    assert high["power_dbm"] > low["power_dbm"]
