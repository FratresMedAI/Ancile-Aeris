#!/usr/bin/env python3
"""Offline labeled eval for acoustic / RF heuristics (Phase 2)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SENSORS = ROOT / "src" / "clearsky_os_sensors"
sys.path.insert(0, str(SENSORS))

from clearsky_os_sensors.acoustic_classifier import (  # noqa: E402
    classify_acoustic,
    synthetic_rotor_waveform,
)
from clearsky_os_sensors.rf_classifier import classify_rf, synthetic_iq  # noqa: E402


def _accuracy(scores_labels: list[tuple[float, int]], threshold: float = 0.45) -> float:
    correct = 0
    for score, label in scores_labels:
        pred = 1 if score >= threshold else 0
        if pred == label:
            correct += 1
    return correct / max(1, len(scores_labels))


def main() -> int:
    acoustic_pairs: list[tuple[float, int]] = []
    rf_pairs: list[tuple[float, int]] = []
    for tick in range(20):
        for present, label in ((True, 1), (False, 0)):
            a = classify_acoustic(
                synthetic_rotor_waveform(tick=tick, present=present),
                force_heuristic=True,
            )
            r = classify_rf(synthetic_iq(tick=tick, present=present), force_heuristic=True)
            acoustic_pairs.append((a.confidence, label))
            rf_pairs.append((r.confidence, label))

    report = {
        "acoustic_accuracy_at_0_45": round(_accuracy(acoustic_pairs), 3),
        "rf_accuracy_at_0_45": round(_accuracy(rf_pairs), 3),
        "n_samples": len(acoustic_pairs),
        "backends": {"acoustic": "heuristic_band_energy", "rf": "heuristic_spectral_peak"},
    }
    print(json.dumps(report, indent=2))
    # Soft gate: synthetic labels should be separable
    if report["acoustic_accuracy_at_0_45"] < 0.8 or report["rf_accuracy_at_0_45"] < 0.8:
        print("WARN: accuracy below 0.8 on synthetic set", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
