#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def derive_rf_parameters(score: float) -> dict:
    return {
        "center_frequency_hz": 2_450_000_000.0,
        "bandwidth_hz": 20_000_000.0 + (5_000_000.0 * score),
        "power_dbm": -5.0 + (10.0 * score),
    }


class CognitiveEwNode(Node):
    def __init__(self) -> None:
        super().__init__("cognitive_ew_node")
        self.safety_open = False
        self.latest_effector_plan: dict | None = None
        self.create_subscription(String, "/digital_twin_result", self._on_twin_result, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.create_subscription(String, "/effector/selected_plan", self._on_effector_plan, 20)
        self.pub = self.create_publisher(String, "/cognitive_ew_commands", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_effector_plan(self, msg: String) -> None:
        try:
            self.latest_effector_plan = json.loads(msg.data)
        except json.JSONDecodeError:
            self.latest_effector_plan = None

    def _on_twin_result(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        score = float(payload.get("effectiveness_probability", 0.0))
        params = derive_rf_parameters(score if self.safety_open else 0.0)

        plan = self.latest_effector_plan or {}
        selected = plan.get("selected", {}) if isinstance(plan, dict) else {}
        mode = selected.get("mode", "monitor")
        family = selected.get("family", "passive")
        rationale = selected.get("rationale", "no effector plan available; defaulting to monitor")
        monitor_only = (not self.safety_open) or bool(selected.get("monitor_only", True))

        out = {
            "command_id": payload.get("proposal_id", "unknown"),
            "strategy": "monitor" if monitor_only else f"recommend_{mode}_human_vetted",
            "selected_effector_mode": mode,
            "effector_family": family,
            "effector_plan_id": plan.get("plan_id") if isinstance(plan, dict) else None,
            "xai_rationale": rationale,
            "requires_human_authorization": not monitor_only,
            "monitor_only": monitor_only,
            **params,
        }
        self.pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = CognitiveEwNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
