from __future__ import annotations

from math import sqrt
from typing import Any, Dict


class PredictionNode:
    def predict(self, kinematics: Dict[str, Any], horizon_s: float = 2.0) -> Dict[str, Any]:
        x = float(kinematics.get("x", 0.0))
        y = float(kinematics.get("y", 0.0))
        vx = float(kinematics.get("vx", 0.0))
        vy = float(kinematics.get("vy", 0.0))
        crowd_density = float(kinematics.get("crowd_density", 0.0))

        speed = sqrt(vx * vx + vy * vy)
        pred_x = x + vx * horizon_s
        pred_y = y + vy * horizon_s

        collision_risk = max(0.0, min(1.0, 0.55 * min(speed / 12.0, 1.0) + 0.45 * crowd_density))

        return {
            "speed_mps": speed,
            "predicted_xy": [pred_x, pred_y],
            "collision_risk": collision_risk,
            "trajectory_horizon_s": horizon_s,
        }
