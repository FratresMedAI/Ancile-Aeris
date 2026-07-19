#!/usr/bin/env python3
"""Offline CV-EKF eval against a synthetic ground-truth trajectory."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

# Allow running without sourcing ROS install
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "clearsky_os_fusion"))

from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF  # noqa: E402


def rmse(xs: list[float], ys: list[float]) -> float:
    if not xs:
        return float("inf")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(xs, ys)) / len(xs))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        default="tests/fixtures/fusion_synth_track.json",
        help="JSON fixture with gt + noisy measurements",
    )
    parser.add_argument("--out", default="reports/fusion_eval.json")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    if not fixture_path.is_file():
        fixture_path = ROOT / args.fixture
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    dt = float(data.get("dt", 0.1))
    measurements = data["measurements"]
    gt = data["ground_truth"]

    ekf = ConstantVelocityEKF(dt=dt, process_var=1.5, measure_var=0.05)
    est_x: list[float] = []
    est_y: list[float] = []
    gt_x = [float(p["x"]) for p in gt]
    gt_y = [float(p["y"]) for p in gt]

    for m in measurements:
        ekf.predict(dt)
        ekf.update(float(m["x"]), float(m["y"]))
        s = ekf.state()
        est_x.append(s["x"])
        est_y.append(s["y"])

    # Align lengths
    n = min(len(est_x), len(gt_x))
    report = {
        "fixture": str(fixture_path),
        "samples": n,
        "rmse_x": rmse(est_x[:n], gt_x[:n]),
        "rmse_y": rmse(est_y[:n], gt_y[:n]),
        "final_confidence": ekf.calibrated_confidence(0.8),
        "method": "constant_velocity_ekf",
    }
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
