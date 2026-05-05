#!/usr/bin/env python3
import json
import time

import rclpy
from ancile_aeris_integration import AncileAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def update_mode(safety_open: bool) -> str:
    return "observe_only" if not safety_open else "bounded_adaptation_stub"


class ContinualLearningNode(Node):
    def __init__(self) -> None:
        super().__init__("continual_learning_node")
        self.safety_open = False
        self.audit_bridge = AncileAuditBridge(self, "continual_learning")
        self.create_subscription(String, "/fused_tracks", self._on_fused, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/continual_learning/status", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_fused(self, msg: String) -> None:
        # TODO: implement constrained online learner with rollback and drift controls.
        _ = msg
        out = {
            "model_name": "threat_model_stub",
            "mode": update_mode(self.safety_open),
            "update_applied": self.safety_open,
            "reason": "safety_gate_closed" if not self.safety_open else f"bounded_update_{int(time.time())}",
        }
        self.pub.publish(String(data=json.dumps(out)))
        self.audit_bridge.emit(
            "continual_learning_status",
            out,
            xai_text="Continual learning remains bounded and safety-constrained.",
        )


def main() -> None:
    rclpy.init()
    node = ContinualLearningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
