"""Analytic kinematics / collateral risk for proposed mitigations."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class TwinEvaluation:
    effectiveness_probability: float
    collateral_risk_score: float
    veto: bool
    risk: float
    closing_speed_mps: float
    miss_distance_m: float
    rationale: str


def evaluate_proposal(
    *,
    track_x: float = 0.0,
    track_y: float = 0.0,
    track_vx: float = 0.0,
    track_vy: float = 0.0,
    threat_score: float = 0.5,
    mitigation_gain: float = 0.6,
    asset_x: float = 0.0,
    asset_y: float = 0.0,
    asset_radius_m: float = 25.0,
    risk_veto_threshold: float = 0.65,
    safety_open: bool = False,
) -> TwinEvaluation:
    """Point-mass closing geometry + simple collateral disk."""
    dx = float(track_x) - float(asset_x)
    dy = float(track_y) - float(asset_y)
    range_m = math.hypot(dx, dy)
    speed = math.hypot(float(track_vx), float(track_vy))

    # Closing component toward asset (positive = approaching)
    if range_m > 1e-6:
        closing = -(dx * float(track_vx) + dy * float(track_vy)) / range_m
    else:
        closing = speed

    miss = max(0.0, range_m - float(asset_radius_m))
    proximity_risk = max(0.0, min(1.0, 1.0 - miss / max(asset_radius_m * 4.0, 1.0)))
    approach_risk = max(0.0, min(1.0, closing / 40.0)) if closing > 0 else 0.0
    threat = max(0.0, min(1.0, float(threat_score)))
    gain = max(0.0, min(1.0, float(mitigation_gain)))
    if not safety_open:
        gain *= 0.35

    effectiveness = max(0.0, min(1.0, 0.45 * threat + 0.55 * gain))
    collateral = max(0.0, min(1.0, 0.5 * proximity_risk + 0.3 * approach_risk + 0.2 * (1.0 - effectiveness)))
    risk = collateral
    veto = risk >= float(risk_veto_threshold)

    rationale = (
        f"analytic twin: range={range_m:.1f}m closing={closing:.1f}m/s "
        f"risk={risk:.2f} veto={veto}"
    )
    return TwinEvaluation(
        effectiveness_probability=effectiveness,
        collateral_risk_score=collateral,
        veto=veto,
        risk=risk,
        closing_speed_mps=closing,
        miss_distance_m=miss,
        rationale=rationale,
    )
