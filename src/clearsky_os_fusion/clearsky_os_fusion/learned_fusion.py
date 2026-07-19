"""Calibrated ranking model for measurement association (shadow fusion).

Not a deep network — a logistic scorer fit conceptually on synthetic multimodal
replay. Authoritative tracks remain CV-EKF; this ranks candidates and can drive
a parallel shadow filter published on /fusion/learned_tracks.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF, Measurement


# Feature order: confidence, inv_maha, is_visual, is_thermal, is_lidar, is_acoustic, is_rf
_WEIGHTS = [2.4, 1.6, 0.9, 0.7, 0.8, 0.45, 0.4]
_BIAS = -1.1

_MODALITY_IDX = {
    "visual": 2,
    "thermal": 3,
    "lidar": 4,
    "acoustic": 5,
    "rf": 6,
    "position": 2,
}


def _sigmoid(x: float) -> float:
    if x >= 20.0:
        return 1.0
    if x <= -20.0:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def measurement_features(m: Measurement, mahalanobis: float) -> list[float]:
    inv_maha = 1.0 / (1.0 + max(0.0, float(mahalanobis)))
    feats = [float(m.confidence), inv_maha, 0.0, 0.0, 0.0, 0.0, 0.0]
    idx = _MODALITY_IDX.get(str(m.modality), None)
    if idx is not None:
        feats[idx] = 1.0
    return feats


def score_measurement(m: Measurement, mahalanobis: float) -> float:
    feats = measurement_features(m, mahalanobis)
    z = _BIAS + sum(w * f for w, f in zip(_WEIGHTS, feats))
    return _sigmoid(z)


@dataclass
class RankedMeasurement:
    measurement: Measurement
    score: float
    mahalanobis: float


def rank_measurements(
    ekf: ConstantVelocityEKF,
    measurements: Iterable[Measurement],
) -> list[RankedMeasurement]:
    ranked: list[RankedMeasurement] = []
    for m in measurements:
        d = 0.0 if not ekf.initialized else ekf.mahalanobis(m.x, m.y)
        ranked.append(RankedMeasurement(measurement=m, score=score_measurement(m, d), mahalanobis=d))
    ranked.sort(key=lambda r: r.score, reverse=True)
    return ranked


def shadow_associate(
    ekf: ConstantVelocityEKF,
    measurements: list[Measurement],
    *,
    min_score: float = 0.35,
) -> Measurement | None:
    """Pick highest learned score (optionally gated by score floor)."""
    pool = list(measurements)
    if not ekf.initialized and pool:
        # Same geometric pre-gate as CV associate on first fix
        ranges = [math.hypot(m.x, m.y) for m in pool]
        med = sorted(ranges)[len(ranges) // 2]
        limit = max(med * 2.5, 50.0)
        gated = [m for m in pool if math.hypot(m.x, m.y) <= limit]
        pool = gated or pool
    else:
        # Soft mahalanobis prefilter once initialized
        gated = [m for m in pool if ekf.mahalanobis(m.x, m.y) <= 8.0]
        pool = gated or pool
    ranked = rank_measurements(ekf, pool)
    if not ranked:
        return None
    best = ranked[0]
    if best.score < min_score:
        return None
    return best.measurement


def run_shadow_step(
    shadow_ekf: ConstantVelocityEKF,
    measurements: list[Measurement],
    dt: float,
    *,
    min_score: float = 0.35,
) -> dict[str, float]:
    shadow_ekf.predict(dt)
    chosen = shadow_associate(shadow_ekf, measurements, min_score=min_score)
    meas_conf = 0.0
    score = 0.0
    if chosen is not None:
        score = score_measurement(
            chosen,
            0.0 if not shadow_ekf.initialized else shadow_ekf.mahalanobis(chosen.x, chosen.y),
        )
        shadow_ekf.update(chosen.x, chosen.y)
        meas_conf = chosen.confidence
    state = shadow_ekf.state()
    conf = shadow_ekf.calibrated_confidence(max(meas_conf, score))
    return {
        **state,
        "confidence": conf,
        "learned_score": score,
        "updated": 1.0 if chosen is not None else 0.0,
    }
