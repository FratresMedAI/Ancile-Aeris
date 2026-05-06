from __future__ import annotations

from typing import Any, Dict


class TriageNode:
    def score(self, medical: Dict[str, Any], detection: Dict[str, Any]) -> Dict[str, Any]:
        temp_delta = float(medical.get("temp_delta", 0.0))
        perfusion_proxy = float(medical.get("perfusion_proxy", 0.0))
        motion_stability = float(medical.get("motion_stability", 0.0))
        victim_score = float(detection.get("victim_score", 0.0))

        risk = max(0.0, min(1.0, 0.35 * temp_delta + 0.30 * perfusion_proxy + 0.20 * (1 - motion_stability) + 0.15 * victim_score))

        if risk >= 0.85:
            priority = "immediate"
        elif risk >= 0.65:
            priority = "delayed"
        elif risk >= 0.4:
            priority = "minimal"
        else:
            priority = "expectant"

        return {"triage_risk": risk, "triage_priority": priority}
