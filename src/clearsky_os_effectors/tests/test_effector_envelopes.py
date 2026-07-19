"""Unit tests for analytic effector envelopes."""

from __future__ import annotations

import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_effectors.envelopes import (  # noqa: E402
    friis_path_loss_db,
    success_probability,
    track_range_m,
)


def test_friis_increases_with_range() -> None:
    assert friis_path_loss_db(100.0) < friis_path_loss_db(1000.0)


def test_jamming_success_drops_with_range() -> None:
    near = success_probability("cognitive_jamming", 200.0, readiness=1.0)
    far = success_probability("cognitive_jamming", 8000.0, readiness=1.0)
    assert near["success_probability"] > far["success_probability"]
    assert near["path_loss_db"] < far["path_loss_db"]


def test_track_range() -> None:
    r = track_range_m({"x": 300.0, "y": 400.0, "z": 0.0})
    assert abs(r - 500.0) < 1e-6
