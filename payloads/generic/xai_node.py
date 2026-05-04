from __future__ import annotations

from typing import Any, Dict


class XAINode:
    def explain(self, fused: Dict[str, Any], detection: Dict[str, Any], triage: Dict[str, Any], safety: Dict[str, Any]) -> Dict[str, Any]:
        top_signal = fused.get("dominant_signal", "unknown")
        victim_score = float(detection.get("victim_score", 0.0))
        triage_risk = float(triage.get("triage_risk", 0.0))
        blocked_reasons = safety.get("reasons", [])

        explanation = {
            "decision_summary": "alert_recommended" if safety.get("allow") else "held_for_safety",
            "top_sensor_contributor": top_signal,
            "victim_score": victim_score,
            "triage_risk": triage_risk,
            "safety_reasons": blocked_reasons,
            "plain_english": (
                f"Primary evidence came from {top_signal}; victim score={victim_score:.2f}, "
                f"triage risk={triage_risk:.2f}."
            ),
        }
        return explanation
