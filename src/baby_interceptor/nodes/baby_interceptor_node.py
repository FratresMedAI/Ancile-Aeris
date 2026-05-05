#!/usr/bin/env python3
import json
import time

import rclpy
from darkspace_integration import AncileAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


class BabyInterceptorNode(Node):
    def __init__(self) -> None:
        super().__init__("baby_interceptor_node")
        self.safety_open = False
        self.launch_authorized = False
        self.terminal_authorized = False
        self.audit_bridge = AncileAuditBridge(self, "baby_interceptor")
        self.create_subscription(String, "/interceptor_handoff", self._on_handoff, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, 20)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, 20)
        self.create_subscription(String, "/operator/terminal_authorizations", self._on_terminal_auth, 20)
        self.status_pub = self.create_publisher(String, "/interceptor_status", 20)
        self.result_pub = self.create_publisher(String, "/engagement_result", 20)
        self.audit_pub = self.create_publisher(String, "/audit/events", 20)

    def _on_safety(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_launch_auth(self, msg: String) -> None:
        try:
            self.launch_authorized = bool(json.loads(msg.data).get("approved", False))
        except json.JSONDecodeError:
            self.launch_authorized = False

    def _on_terminal_auth(self, msg: String) -> None:
        try:
            self.terminal_authorized = bool(json.loads(msg.data).get("approved", False))
        except json.JSONDecodeError:
            self.terminal_authorized = False

    def _on_handoff(self, msg: String) -> None:
        # TODO: integrate onboard guidance and low-collateral effector models.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        auth_path_ok = (
            self.safety_open
            and self.launch_authorized
            and self.terminal_authorized
            and bool(payload.get("release_authorized", False))
        )
        status = {
            "interceptor_id": "baby-int-001",
            "state": "engage_stub" if auth_path_ok else "monitor_hold",
            "launch_authorized": self.launch_authorized,
            "terminal_authorized": self.terminal_authorized,
            "notes": "double_human_auth_required",
        }
        self.status_pub.publish(String(data=json.dumps(status)))
        result = {
            "engagement_id": payload.get("engagement_id", f"eng-{int(time.time())}"),
            "interceptor_id": status["interceptor_id"],
            "outcome": "simulated_disable_stub" if auth_path_ok else "blocked_pending_authorization",
            "collateral_risk": 0.1 if auth_path_ok else 0.0,
            "authorized_path_verified": auth_path_ok,
        }
        self.result_pub.publish(String(data=json.dumps(result)))
        self.audit_pub.publish(String(data=json.dumps({"event": "interceptor_engagement", "result": result})))
        self.audit_bridge.emit(
            "interceptor_engagement",
            result,
            xai_text="Interceptor engagement remains blocked unless safety gate plus double human authorization are both true.",
        )


def main() -> None:
    rclpy.init()
    node = BabyInterceptorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
