#!/usr/bin/env python3
"""Compare authoritative CV-EKF vs learned-association shadow on synthetic multimodal truth."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "clearsky_os_fusion"))
sys.path.insert(0, str(ROOT / "src" / "clearsky_os_sim"))

from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF, Measurement, associate_nearest  # noqa: E402
from clearsky_os_fusion.learned_fusion import run_shadow_step  # noqa: E402
from clearsky_os_sim.kinematics import project_sensors, truth_at  # noqa: E402


def rmse(xs: list[float], ys: list[float]) -> float:
    n = min(len(xs), len(ys))
    if n == 0:
        return float("inf")
    return math.sqrt(sum((xs[i] - ys[i]) ** 2 for i in range(n)) / n)


def main() -> int:
    dt = 0.1
    ekf = ConstantVelocityEKF(dt=dt, process_var=1.5, measure_var=1.0)
    shadow = ConstantVelocityEKF(dt=dt, process_var=1.5, measure_var=1.0)
    gt_x: list[float] = []
    gt_y: list[float] = []
    ekf_x: list[float] = []
    ekf_y: list[float] = []
    sh_x: list[float] = []
    sh_y: list[float] = []

    for i in range(40):
        t = i * dt
        state = truth_at(t)
        proj = project_sensors(state, tick=i)
        measurements: list[Measurement] = []
        for trk in proj["visual"]["tracks"]:
            measurements.append(
                Measurement(trk["x"], trk["y"], trk["confidence"], trk["track_id"], "visual")
            )
        for det in proj["lidar"]["detections"]:
            rad = math.radians(det["bearing_deg"])
            measurements.append(
                Measurement(
                    det["range_m"] * math.cos(rad),
                    det["range_m"] * math.sin(rad),
                    det["confidence"],
                    det["id"],
                    "lidar",
                )
            )
        # Add a clutter outlier
        measurements.append(Measurement(500.0, 500.0, 0.99, "clutter", "visual"))

        ekf.predict(dt)
        chosen = associate_nearest(ekf, measurements, gate=5.0)
        if chosen is not None:
            ekf.update(chosen.x, chosen.y)
        s = ekf.state()
        sh = run_shadow_step(shadow, measurements, dt, min_score=0.3)

        gt_x.append(state.x)
        gt_y.append(state.y)
        ekf_x.append(s["x"])
        ekf_y.append(s["y"])
        sh_x.append(sh["x"])
        sh_y.append(sh["y"])

    report = {
        "samples": len(gt_x),
        "ekf_rmse_x": rmse(ekf_x, gt_x),
        "ekf_rmse_y": rmse(ekf_y, gt_y),
        "learned_shadow_rmse_x": rmse(sh_x, gt_x),
        "learned_shadow_rmse_y": rmse(sh_y, gt_y),
        "authoritative": "constant_velocity_ekf",
        "shadow": "logistic_ranker_v1",
        "note": "Shadow is diagnostic only; /fused_tracks remains EKF-authoritative.",
    }
    out = ROOT / "reports" / "fusion_learned_eval.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    # Soft gate: EKF should track inbound truth better than random
    if report["ekf_rmse_x"] > 30.0:
        print("WARN: EKF RMSE unexpectedly high", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
