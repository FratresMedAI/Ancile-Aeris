"""Deterministic UAS kinematics + sensor projections (Gazebo-compatible protocol).

This is the CI-safe twin/sim backend. The SDF world in worlds/clearsky_cuas.sdf
describes the same scenario for Gazebo Harmonic; the bridge node uses this
kinematics model when gz is not running.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TruthState:
    t: float
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float


def truth_at(
    t: float,
    *,
    x0: float = 180.0,
    y0: float = 40.0,
    z0: float = 60.0,
    vx: float = -12.0,
    vy: float = 2.0,
) -> TruthState:
    """Straight-line inbound track toward asset at origin."""
    return TruthState(
        t=float(t),
        x=x0 + vx * t,
        y=y0 + vy * t,
        z=z0,
        vx=vx,
        vy=vy,
        vz=0.0,
    )


def bearing_deg(x: float, y: float, ox: float = 0.0, oy: float = 0.0) -> float:
    return math.degrees(math.atan2(y - oy, x - ox))


def range_m(x: float, y: float, ox: float = 0.0, oy: float = 0.0) -> float:
    return math.hypot(x - ox, y - oy)


def project_sensors(
    state: TruthState,
    *,
    tick: int = 0,
    noise_pos: float = 1.5,
    noise_bearing_deg: float = 2.0,
) -> dict[str, Any]:
    """Project truth into ClearSky sensor JSON shapes (metric map frame)."""
    # Deterministic pseudo-noise from tick (no RNG dependency)
    n1 = math.sin(0.37 * tick) * noise_pos
    n2 = math.cos(0.29 * tick) * noise_pos
    nb = math.sin(0.41 * tick) * noise_bearing_deg
    brg = bearing_deg(state.x, state.y) + nb
    rng = range_m(state.x, state.y)

    visual = {
        "tracks": [
            {
                "track_id": f"sim-vis-{tick:05d}",
                "cls": "uas",
                "confidence": 0.78,
                "x": state.x + n1,
                "y": state.y + n2,
                "w": 4.0,
                "h": 4.0,
                "source": "visual",
                "position_frame": "map",
                "synthetic": True,
            }
        ],
        "backend": "sim_truth_projection",
    }
    thermal = {
        "tracks": [
            {
                "track_id": f"sim-thm-{tick:05d}",
                "cls": "hot_uas",
                "confidence": 0.70,
                "x": state.x + 0.7 * n2,
                "y": state.y - 0.5 * n1,
                "source": "thermal",
                "position_frame": "map",
                "synthetic": True,
            }
        ],
        "backend": "sim_truth_projection",
    }
    acoustic = {
        "detections": [
            {
                "detection_id": f"sim-aud-{tick:05d}",
                "confidence": 0.62,
                "estimated_bearing_deg": brg,
                "frequency_band_hz": [120.0, 1800.0],
                "source": "acoustic",
                "backend": "sim_truth_projection",
            }
        ],
        "backend": "sim_truth_projection",
    }
    rf = {
        "fingerprints": [
            {
                "emitter_id": f"sim-rf-{tick:05d}",
                "confidence": 0.60,
                "center_freq_hz": 2.437e9,
                "bandwidth_hz": 20.0e6,
                "modulation_guess": "ofdm",
                "estimated_bearing_deg": brg + 0.5 * nb,
                "source": "rf",
                "backend": "sim_truth_projection",
            }
        ],
        "backend": "sim_truth_projection",
    }
    lidar = {
        "detections": [
            {
                "id": f"sim-lid-{tick:05d}",
                "range_m": rng + 0.3 * n1,
                "bearing_deg": brg,
                "confidence": 0.72,
                "synthetic": True,
                "backend": "sim_truth_projection",
            }
        ],
    }
    return {
        "visual": visual,
        "thermal": thermal,
        "acoustic": acoustic,
        "rf": rf,
        "lidar": lidar,
    }


def ground_truth_payload(state: TruthState, tick: int = 0) -> dict[str, Any]:
    return {
        "producer": "clearsky_os_sim",
        "protocol": "gazebo_compatible_v1",
        "tick": tick,
        "frame_id": "map",
        "truth": {
            "t": state.t,
            "x": state.x,
            "y": state.y,
            "z": state.z,
            "vx": state.vx,
            "vy": state.vy,
            "vz": state.vz,
            "entity": "uas_inbound_01",
        },
        "asset": {"x": 0.0, "y": 0.0, "z": 0.0, "radius_m": 25.0},
        "world": "clearsky_cuas.sdf",
    }
