"""Pure scout enrichment helpers (no ROS deps)."""

from __future__ import annotations

from typing import Any, Dict

SCOUT_SOURCE = "clearsky_os_scout_mothership"


def loiter_profile() -> dict:
    return {
        "altitude_m": 4500.0,
        "endurance_hr": 24.0,
        "sensors": ["eo_ir", "rf", "acoustic"],
    }


def coverage_cell_for_xy(x: float, y: float, cell_size_m: float = 250.0) -> str:
    gx = int(x // cell_size_m)
    gy = int(y // cell_size_m)
    return f"grid_{gx}_{gy}"


def enrich_track(track: Dict[str, Any], mothership_id: str, mesh_peers: int) -> Dict[str, Any]:
    """Build scout enrichment overlay from an upstream fused track (no new kinematics)."""
    profile = loiter_profile()
    x = float(track.get("x", 0.0))
    y = float(track.get("y", 0.0))
    conf = float(track.get("confidence", 0.0))
    cell = coverage_cell_for_xy(x, y)
    return {
        "track_id": str(track.get("track_id", "unknown")),
        "source": SCOUT_SOURCE,
        "mothership_id": mothership_id,
        "x": x,
        "y": y,
        "vx": float(track.get("vx", 0.0)),
        "vy": float(track.get("vy", 0.0)),
        "altitude_m": profile["altitude_m"],
        "sensor_type": "high_altitude_eo_ir_rf",
        "confidence": conf,
        "upstream_confidence": conf,
        "class_label": str(track.get("class_label", "fused_track")),
        "coverage_cell": cell,
        "mesh": {
            "mothership_id": mothership_id,
            "peer_count_hint": mesh_peers,
            "role": "enrichment_only",
        },
        "notes": "scout_enrichment_of_fused_track",
        "invents_track": False,
    }
