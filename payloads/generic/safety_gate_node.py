from __future__ import annotations

from typing import Any, Dict, Tuple

try:
    from clearsky_rule_guard import classify_text
except ImportError:  # pragma: no cover - optional when copied as a package module
    classify_text = None  # type: ignore[assignment]


class SafetyGateNode:
    def __init__(self, pid_target: float = 0.999) -> None:
        self.pid_target = pid_target

    def evaluate(self, context: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        # BORAP 04 environmental constraints are applied uniformly. In dense urban,
        # mass-gathering, critical-infrastructure, mobile-platform, and remote-terrain
        # conditions we keep conservative monitor-safe defaults unless safety checks pass.
        fused_conf = float(context.get("fused_confidence", 0.0))
        collision_risk = float(context.get("collision_risk", 0.0))
        pid_score = float(context.get("pid_score", 0.0))
        human_veto = bool(context.get("human_veto", False))
        friendly_iff = bool(context.get("friendly_iff", False))
        jammed = bool(context.get("jammed", False))
        operator_text = str(context.get("operator_text", ""))
        tool_trace = str(context.get("tool_trace", ""))

        reasons = []
        allow = True

        if fused_conf < 0.6:
            allow = False
            reasons.append("low_fusion_confidence")
        if collision_risk > 0.8:
            allow = False
            reasons.append("high_collision_risk")
        if pid_score < self.pid_target:
            allow = False
            reasons.append("pid_below_threshold")
        if human_veto:
            allow = False
            reasons.append("human_veto")
        if friendly_iff:
            allow = False
            reasons.append("friendly_iff_lockout")
        if jammed:
            allow = False
            reasons.append("jamming_detected_offline_hold")
        if classify_text is not None and (operator_text or tool_trace):
            clearsky_verdict = classify_text(operator_text, tool_trace=tool_trace)
            if clearsky_verdict.label == "block":
                allow = False
                reasons.append("clearsky_rule_guard_block")

        return allow, {
            "allow": allow,
            "reasons": reasons,
            "pid_target": self.pid_target,
        }
