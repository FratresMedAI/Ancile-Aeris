"""Short-horizon kinematic rollout twin (Gazebo-compatible backend).

Uses fused (or ground-truth) state to propagate a what-if trajectory and
re-score collateral risk. Does not require a live Gazebo process.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from digital_twin.physics import TwinEvaluation, evaluate_proposal


@dataclass(frozen=True)
class RolloutConfig:
    horizon_s: float = 3.0
    dt: float = 0.2
    asset_x: float = 0.0
    asset_y: float = 0.0
    asset_radius_m: float = 25.0
    risk_veto_threshold: float = 0.65


def propagate(
    x: float,
    y: float,
    vx: float,
    vy: float,
    *,
    horizon_s: float,
    dt: float,
) -> list[tuple[float, float, float, float]]:
    """Constant-velocity rollout samples (x, y, vx, vy)."""
    samples: list[tuple[float, float, float, float]] = []
    t = 0.0
    cx, cy = float(x), float(y)
    while t <= float(horizon_s) + 1e-9:
        samples.append((cx, cy, float(vx), float(vy)))
        cx += float(vx) * float(dt)
        cy += float(vy) * float(dt)
        t += float(dt)
    return samples


def evaluate_rollout(
    *,
    track_x: float,
    track_y: float,
    track_vx: float,
    track_vy: float,
    threat_score: float = 0.5,
    mitigation_gain: float = 0.6,
    safety_open: bool = False,
    truth_x: float | None = None,
    truth_y: float | None = None,
    cfg: RolloutConfig | None = None,
) -> TwinEvaluation:
    """Roll out kinematics; take max risk along horizon; blend with analytic now-cast."""
    cfg = cfg or RolloutConfig()
    now = evaluate_proposal(
        track_x=track_x,
        track_y=track_y,
        track_vx=track_vx,
        track_vy=track_vy,
        threat_score=threat_score,
        mitigation_gain=mitigation_gain,
        asset_x=cfg.asset_x,
        asset_y=cfg.asset_y,
        asset_radius_m=cfg.asset_radius_m,
        risk_veto_threshold=cfg.risk_veto_threshold,
        safety_open=safety_open,
    )

    # Prefer truth position for rollout origin when available (sim twin)
    ox = float(truth_x) if truth_x is not None else float(track_x)
    oy = float(truth_y) if truth_y is not None else float(track_y)
    samples = propagate(ox, oy, track_vx, track_vy, horizon_s=cfg.horizon_s, dt=cfg.dt)

    peak_risk = now.risk
    peak_eval = now
    for sx, sy, svx, svy in samples:
        ev = evaluate_proposal(
            track_x=sx,
            track_y=sy,
            track_vx=svx,
            track_vy=svy,
            threat_score=threat_score,
            mitigation_gain=mitigation_gain,
            asset_x=cfg.asset_x,
            asset_y=cfg.asset_y,
            asset_radius_m=cfg.asset_radius_m,
            risk_veto_threshold=cfg.risk_veto_threshold,
            safety_open=safety_open,
        )
        if ev.risk > peak_risk:
            peak_risk = ev.risk
            peak_eval = ev

    truth_note = ""
    if truth_x is not None and truth_y is not None:
        err = math.hypot(float(track_x) - float(truth_x), float(track_y) - float(truth_y))
        truth_note = f" truth_err={err:.1f}m"

    rationale = (
        f"gazebo_rollout twin: horizon={cfg.horizon_s:.1f}s "
        f"peak_risk={peak_eval.risk:.2f} veto={peak_eval.veto}{truth_note}"
    )
    return TwinEvaluation(
        effectiveness_probability=peak_eval.effectiveness_probability,
        collateral_risk_score=peak_eval.collateral_risk_score,
        veto=peak_eval.veto,
        risk=peak_eval.risk,
        closing_speed_mps=peak_eval.closing_speed_mps,
        miss_distance_m=peak_eval.miss_distance_m,
        rationale=rationale,
    )
