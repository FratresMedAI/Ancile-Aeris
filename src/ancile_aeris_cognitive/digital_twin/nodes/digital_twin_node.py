#!/usr/bin/env python3
import json
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def score_effectiveness(threat_score: float, mitigation_gain: float) -> tuple[float, float]:
    effectiveness = min(1.0, max(0.0, 0.5 * threat_score + 0.5 * mitigation_gain))
    collateral = max(0.0, 1.0 - effectiveness)
    return effectiveness, collateral


class DigitalTwinNode(Node):
    def __init__(self) -> None:
        super().__init__("digital_twin_node")
        self.safety_open = False
        self.create_subscription(String, "/proposed_actions", self._on_proposal, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.result_pub = self.create_publisher(String, "/digital_twin_result", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_proposal(self, msg: String) -> None:
        start = time.perf_counter()
        # TODO: integrate real physics and optional Gazebo simulation path.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        effectiveness, collateral = score_effectiveness(float(payload.get("score", 0.5)), 0.6 if self.safety_open else 0.2)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        out = {"proposal_id": payload.get("proposal_id", "unknown"), "effectiveness_probability": effectiveness, "collateral_risk_score": collateral, "latency_ms": elapsed_ms}
        self.result_pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = DigitalTwinNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
