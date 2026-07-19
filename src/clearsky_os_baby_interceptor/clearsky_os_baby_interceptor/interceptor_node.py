#!/usr/bin/env python3
"""ClearSky OS simulation-only baby interceptor (human authorized defensive flow)."""

import json
import time

import rclpy
from clearsky_os_integration import ClearSkyAuditBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


def auth_path_ok(safety_open: bool, launch: bool, terminal: bool, release_authorized: bool, require_double_auth: bool) -> bool:
    if require_double_auth:
        return safety_open and launch and terminal and release_authorized
    return safety_open and launch and release_authorized


class BabyInterceptorNode(Node):
    def __init__(self) -> None:
        super().__init__("clearsky_os_baby_interceptor_node")
        self.declare_parameter("require_simulate_only_deploy_cmd", False)
        self.declare_parameter("require_double_authorization", True)

        self.safety_open = False
        self.launch_authorized = False
        self.terminal_authorized = False
        self.simulate_only_deploy_registered = False
        self.audit_bridge = ClearSkyAuditBridge(self, "clearsky_os_baby_interceptor")

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(String, "/interceptor_handoff", self._on_handoff, reliable_qos)
        self.create_subscription(String, "/interceptor_deploy_cmd", self._on_deploy_cmd, reliable_qos)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, reliable_qos)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, reliable_qos)
        self.create_subscription(String, "/operator/terminal_authorizations", self._on_terminal_auth, reliable_qos)
        self.status_pub = self.create_publisher(String, "/interceptor_status", reliable_qos)
        self.result_pub = self.create_publisher(String, "/engagement_result", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)
        self.get_logger().info("clearsky_os_baby_interceptor_node initialized")

    def _require_deploy_cmd_gate(self) -> bool:
        return bool(self.get_parameter("require_simulate_only_deploy_cmd").value)

    def _require_double_auth(self) -> bool:
        return bool(self.get_parameter("require_double_authorization").value)

    def _on_deploy_cmd(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("Ignoring non-JSON interceptor deploy command")
            return

        if not payload.get("simulate_only", False):
            self.get_logger().info("Deploy command rejected: simulate_only must be true")
            return

        self.simulate_only_deploy_registered = True
        ack = {
            "interceptor_id": "baby-int-sim-001",
            "state": "simulate_only_deploy_command_registered",
            "mode": "simulation_only",
            "notes": "Human-gated defensive simulation path; no autonomous release.",
        }
        self.status_pub.publish(String(data=json.dumps(ack)))
        self.audit_pub.publish(String(data=json.dumps({"event": "interceptor_deploy_cmd", "command": payload})))
        self.audit_bridge.emit(
            "interceptor_deploy_cmd",
            ack,
            xai_text="Simulator-only deployment command acknowledged; engagement remains human-gated.",
        )

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
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return

        deploy_gate_ok = (not self._require_deploy_cmd_gate()) or self.simulate_only_deploy_registered
        release_authorized = bool(payload.get("release_authorized", False))
        allowed = deploy_gate_ok and auth_path_ok(
            self.safety_open,
            self.launch_authorized,
            self.terminal_authorized,
            release_authorized,
            self._require_double_auth(),
        )

        status = {
            "interceptor_id": "baby-int-sim-001",
            "engagement_id": payload.get("engagement_id", f"eng-{int(time.time())}"),
            "track_id": payload.get("track_id", "unknown"),
            "state": "simulated_intercept_complete" if allowed else "hold_pending_authorization",
            "mode": "simulation_only",
            "safety_gate_open": self.safety_open,
            "launch_authorized": self.launch_authorized,
            "terminal_authorized": self.terminal_authorized,
            "simulate_only_deploy_registered": self.simulate_only_deploy_registered,
            "release_authorized": release_authorized,
            "double_authorization_required": self._require_double_auth(),
        }
        result = {
            "engagement_id": status["engagement_id"],
            "interceptor_id": status["interceptor_id"],
            "outcome": "simulated_disable" if allowed else "blocked_by_human_authorization_gate",
            "authorized_path_verified": allowed,
            "collateral_risk": 0.0,
            "notes": "No autonomous deployment; simulator-safe status event only.",
        }
        self.status_pub.publish(String(data=json.dumps(status)))
        self.result_pub.publish(String(data=json.dumps(result)))
        self.audit_pub.publish(String(data=json.dumps({"event": "interceptor_engagement", "result": result})))
        self.audit_bridge.emit(
            "interceptor_engagement",
            result,
            xai_text="Interceptor remains blocked unless safety, launch authorization, and required human consents are satisfied.",
        )


def main() -> None:
    rclpy.init()
    node = BabyInterceptorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

