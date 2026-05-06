from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AutonomyPolicy:
    threat_follow_threshold: float = 0.72
    high_risk_threshold: float = 0.68


class AutonomyNode:
    def __init__(self, policy: AutonomyPolicy | None = None) -> None:
        self.policy = policy or AutonomyPolicy()

    def recommend(
        self,
        detection: Dict[str, Any],
        prediction: Dict[str, Any],
        triage: Dict[str, Any],
        safety: Dict[str, Any],
        control: Dict[str, Any],
    ) -> Dict[str, Any]:
        if safety.get("decision") == "hold":
            return {
                "mode": "hold_safe",
                "actions": ["maintain_standoff", "operator_review_required"],
                "cloud_event": "hold_safety_event",
            }

        detect_score = float(detection.get("detection_score", 0.0))
        risk = float(prediction.get("collision_risk", 0.0))
        priority = str(triage.get("priority", "minimal"))

        actions = ["publish_geotagged_alert"]
        if detect_score >= self.policy.threat_follow_threshold:
            actions.extend(["auto_loiter", "auto_zoom"])
        if risk >= self.policy.high_risk_threshold:
            actions.append("discreet_follow")

        escalation = "routine"
        if priority == "immediate" or control.get("jammed", False):
            escalation = "critical"
            actions.append("dispatch_security_interdiction_ready")

        return {
            "mode": "monitor",
            "actions": actions,
            "escalation": escalation,
            "cloud_event": "counterterror_perimeter_threat_alert",
        }
