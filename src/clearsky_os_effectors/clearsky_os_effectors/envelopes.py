"""Analytic non-kinetic effector envelopes (path-loss / success probability).

These are physics-informed planning aids for simulation and XAI — not hardware
actuation models. Policy selection remains in effector_policy_node.
"""

from __future__ import annotations

import math
from typing import Any, Dict


# Nominal RF carrier used for Friis-style link estimates (control-link band).
DEFAULT_FREQ_HZ = 2.4e9
C_LIGHT = 2.99792458e8

# Mode-specific effective isotropic radiated power / coupling stubs (dBm / unitless).
MODE_PARAMS: Dict[str, Dict[str, float]] = {
    "monitor": {"eirp_dbm": -100.0, "coupling": 0.0, "max_range_m": 0.0},
    "multi_sensor_deception": {"eirp_dbm": 20.0, "coupling": 0.35, "max_range_m": 2500.0},
    "cognitive_jamming": {"eirp_dbm": 37.0, "coupling": 0.55, "max_range_m": 4000.0},
    "gnss_link_spoofing": {"eirp_dbm": 30.0, "coupling": 0.40, "max_range_m": 3000.0},
    "hpm_denial_stub": {"eirp_dbm": 55.0, "coupling": 0.70, "max_range_m": 1500.0},
    "control_link_takeover": {"eirp_dbm": 33.0, "coupling": 0.50, "max_range_m": 2000.0},
    "kamikaze_ram": {"eirp_dbm": -100.0, "coupling": 0.0, "max_range_m": 800.0},
}


def friis_path_loss_db(range_m: float, freq_hz: float = DEFAULT_FREQ_HZ) -> float:
    """Free-space path loss (dB). Clamps range to avoid log singularity."""
    r = max(1.0, float(range_m))
    lam = C_LIGHT / max(1.0, float(freq_hz))
    return 20.0 * math.log10(4.0 * math.pi * r / lam)


def received_power_dbm(
    range_m: float,
    eirp_dbm: float,
    freq_hz: float = DEFAULT_FREQ_HZ,
    rx_gain_db: float = 0.0,
) -> float:
    return float(eirp_dbm) - friis_path_loss_db(range_m, freq_hz) + float(rx_gain_db)


def logistic(x: float) -> float:
    # Stable logistic
    if x >= 20.0:
        return 1.0
    if x <= -20.0:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def track_range_m(track: Dict[str, Any], origin_xy: tuple[float, float] = (0.0, 0.0)) -> float:
    x = float(track.get("x", 0.0))
    y = float(track.get("y", 0.0))
    z = float(track.get("z", track.get("altitude_m", 0.0)) or 0.0)
    dx = x - origin_xy[0]
    dy = y - origin_xy[1]
    return math.sqrt(dx * dx + dy * dy + z * z)


def success_probability(
    mode: str,
    range_m: float,
    readiness: float = 1.0,
    *,
    freq_hz: float = DEFAULT_FREQ_HZ,
    noise_floor_dbm: float = -90.0,
) -> Dict[str, float]:
    """Return analytic envelope metrics for a mode at a given slant range."""
    params = MODE_PARAMS.get(mode, MODE_PARAMS["monitor"])
    max_r = float(params["max_range_m"])
    if mode == "monitor" or max_r <= 0.0:
        return {
            "success_probability": 0.0,
            "path_loss_db": friis_path_loss_db(range_m, freq_hz),
            "rx_power_dbm": -200.0,
            "snr_db": -100.0,
            "range_m": float(range_m),
            "max_range_m": max_r,
        }
    if mode == "kamikaze_ram":
        # Geometric intercept feasibility stub (not RF)
        ratio = max(0.0, 1.0 - float(range_m) / max_r)
        p = max(0.0, min(1.0, ratio * float(readiness)))
        return {
            "success_probability": p,
            "path_loss_db": 0.0,
            "rx_power_dbm": 0.0,
            "snr_db": 0.0,
            "range_m": float(range_m),
            "max_range_m": max_r,
        }

    pl = friis_path_loss_db(range_m, freq_hz)
    rx = received_power_dbm(range_m, float(params["eirp_dbm"]), freq_hz)
    snr = rx - float(noise_floor_dbm)
    # Couple SNR and readiness into a soft success curve
    coupling = float(params["coupling"])
    p = logistic((snr - 6.0) / 4.0) * coupling * max(0.0, min(1.0, float(readiness)))
    # Hard range fade
    if range_m > max_r:
        p *= max(0.0, 1.0 - (range_m - max_r) / max(1.0, max_r))
    return {
        "success_probability": max(0.0, min(1.0, p)),
        "path_loss_db": pl,
        "rx_power_dbm": rx,
        "snr_db": snr,
        "range_m": float(range_m),
        "max_range_m": max_r,
    }


def envelopes_for_catalog(
    range_m: float,
    readiness_by_mode: Dict[str, float] | None = None,
) -> Dict[str, Dict[str, float]]:
    readiness_by_mode = readiness_by_mode or {}
    out: Dict[str, Dict[str, float]] = {}
    for mode in MODE_PARAMS:
        ready = float(readiness_by_mode.get(mode, 1.0))
        out[mode] = success_probability(mode, range_m, ready)
    return out
