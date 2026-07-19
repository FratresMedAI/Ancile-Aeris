"""Unit tests for acoustic / RF classifiers (no ROS required)."""

from __future__ import annotations

import sys
from pathlib import Path

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_sensors.acoustic_classifier import (  # noqa: E402
    classify_acoustic,
    synthetic_rotor_waveform,
)
from clearsky_os_sensors.rf_classifier import classify_rf, synthetic_iq  # noqa: E402


def test_acoustic_present_scores_above_absent() -> None:
    present = classify_acoustic(synthetic_rotor_waveform(present=True), force_heuristic=True)
    absent = classify_acoustic(synthetic_rotor_waveform(present=False), force_heuristic=True)
    assert present.backend == "heuristic_band_energy"
    assert present.confidence > absent.confidence
    assert present.confidence < 0.95  # honest mid-band, not fake 0.999


def test_rf_present_scores_above_absent() -> None:
    present = classify_rf(synthetic_iq(present=True), force_heuristic=True)
    absent = classify_rf(synthetic_iq(present=False), force_heuristic=True)
    assert present.backend == "heuristic_spectral_peak"
    assert present.confidence > absent.confidence
    assert present.confidence < 0.95
