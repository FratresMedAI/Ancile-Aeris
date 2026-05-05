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
        self.create_subscription(String, "/digital_twin_result", self._on_twin_result, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/cognitive_ew_commands", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_twin_result(self, msg: String) -> None:
        # TODO: replace with adaptive policy that learns from engagement outcomes.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        score = float(payload.get("effectiveness_probability", 0.0))
        params = derive_rf_parameters(score if self.safety_open else 0.0)
        out = {
            "command_id": payload.get("proposal_id", "unknown"),
            "strategy": "monitor" if not self.safety_open else "recommend_human_vetted_deception_stub",
            "requires_human_authorization": self.safety_open,
            "monitor_only": not self.safety_open,
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
