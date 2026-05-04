#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def verify_action(pid_score: float, pid_gate: float, human_veto_possible: bool) -> tuple[bool, str]:
    if not human_veto_possible:
        return False, "human_veto_unavailable"
    if pid_score < pid_gate:
        return False, "pid_threshold_not_met"
    return True, "verified"


class VerificationNode(Node):
    def __init__(self) -> None:
        super().__init__("verification_node")
        self.safety_open = False
        self.declare_parameter("pid_gate", 0.999)
        self.create_subscription(String, "/proposed_actions", self._on_proposed_action, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.violation_pub = self.create_publisher(String, "/safety_violation", 20)
        self.verified_pub = self.create_publisher(String, "/verified_action", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_proposed_action(self, msg: String) -> None:
        # TODO: expand into formal runtime temporal/property monitors.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        pid_gate = float(self.get_parameter("pid_gate").value)
        pid_score = float(payload.get("score", 0.0))
        verified, reason = verify_action(pid_score, pid_gate, True)
        if not self.safety_open:
            verified, reason = False, "blocked_by_safety_gate_status"
        out = {"action_id": payload.get("proposal_id", "unknown"), "proposal_id": payload.get("proposal_id", "unknown"), "approved_action": payload.get("action", "monitor"), "verified": verified, "verification_reason": reason}
        if verified:
            self.verified_pub.publish(String(data=json.dumps(out)))
        else:
            self.violation_pub.publish(String(data=json.dumps({"violation_id": out["action_id"], "property_name": "safety_gate_and_pid", "severity": "high", "details": reason, "action_blocked": True})))


def main() -> None:
    rclpy.init()
    node = VerificationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
