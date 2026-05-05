#!/usr/bin/env python3
import json

import rclpy
from ancile_aeris_integration import AncileAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def counterfactual_summary(delay_seconds: float) -> str:
    return f"If action occurred {delay_seconds:.1f}s earlier, projected risk would be reduced in this stub model."


class CausalXaiNode(Node):
    def __init__(self) -> None:
        super().__init__("causal_xai_node")
        self.safety_open = False
        self.audit_bridge = AncileAuditBridge(self, "causal_xai")
        self.create_subscription(String, "/digital_twin_result", self._on_result, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/xai/causal_explanations", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_result(self, msg: String) -> None:
        # TODO: replace with structural causal model and robust counterfactual engine.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        out = {
            "action_id": payload.get("proposal_id", "unknown"),
            "causal_summary": "Higher confidence and lower collateral risk increase verification likelihood.",
            "counterfactual_summary": counterfactual_summary(8.0),
            "confidence": 0.74,
            "monitor_only": not self.safety_open,
        }
        self.pub.publish(String(data=json.dumps(out)))
        self.audit_bridge.emit(
            "causal_explanation",
            out,
            xai_text=out["counterfactual_summary"],
        )


def main() -> None:
    rclpy.init()
    node = CausalXaiNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
