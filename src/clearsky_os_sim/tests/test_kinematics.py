import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PKG))

from clearsky_os_sim.kinematics import project_sensors, truth_at  # noqa: E402


def test_truth_moves_inbound() -> None:
    a = truth_at(0.0)
    b = truth_at(5.0)
    assert b.x < a.x
    assert abs(b.vx + 12.0) < 1e-9


def test_project_sensors_map_frame() -> None:
    state = truth_at(1.0)
    proj = project_sensors(state, tick=3)
    assert proj["visual"]["tracks"][0]["position_frame"] == "map"
    assert "estimated_bearing_deg" in proj["acoustic"]["detections"][0]
    assert proj["lidar"]["detections"][0]["range_m"] > 0.0
