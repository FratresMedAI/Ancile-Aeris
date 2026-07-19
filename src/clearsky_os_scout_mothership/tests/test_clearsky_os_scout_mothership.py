"""Tests for clearsky_os_scout_mothership enrichment helpers (no ROS required)."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_ENRICH = (
    Path(__file__).resolve().parent.parent
    / "clearsky_os_scout_mothership"
    / "scout_enrichment.py"
)
_spec = spec_from_file_location("scout_enrichment", _ENRICH)
assert _spec and _spec.loader
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def test_loiter_profile() -> None:
    profile = _mod.loiter_profile()
    assert profile["altitude_m"] > 1000.0
    assert "eo_ir" in profile["sensors"]


def test_enrich_track_does_not_invent_kinematics() -> None:
    upstream = {
        "track_id": "trk-1",
        "x": 120.0,
        "y": 80.0,
        "vx": 2.0,
        "vy": 1.0,
        "confidence": 0.71,
        "class_label": "uas",
    }
    enriched = _mod.enrich_track(upstream, "mhs-001", 2)
    assert enriched["invents_track"] is False
    assert enriched["x"] == 120.0
    assert enriched["y"] == 80.0
    assert enriched["upstream_confidence"] == 0.71
    assert enriched["coverage_cell"].startswith("grid_")


def test_coverage_cell_stable() -> None:
    assert _mod.coverage_cell_for_xy(10.0, 10.0) == _mod.coverage_cell_for_xy(20.0, 30.0)
