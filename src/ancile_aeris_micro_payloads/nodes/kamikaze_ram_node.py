#!/usr/bin/env python3
"""Simulation-only kamikaze ram: high-speed terminal kinetic-energy impact (no explosive payload).

Strictly software simulation. Requires safety gate + paired human authorizations before any simulated release.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict

import rclpy
from ancile_aeris_integration import AncileAuditBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


def auth_path_ok(
    safety_open: bool,
    launch: bool,
    terminal: bool,
    release_authorized: bool,
    require_double: bool,
) -> bool:
    if require_double:
        return safety_open and launch and terminal and release_authorized
    return safety_open and launch and release_authorized


class KamikazeRamNode(Node):
    def __init__(self) -> None:
        super().__init__("kamikaze_ram_node")
        self.declare_parameter("require_simulate_only_deploy_cmd", True)
        self.declare_parameter("require_double_authorization", True)
        self.declare_parameter("mothership_id", "mhs-001")
        self.declare_parameter("micro_id", "kamikaze-micro-001")

        self.safety_open = False
        self.launch_authorized = False
        self.terminal_authorized = False
        self.simulate_only_deploy_registered = False
        self.latest_effector_mode: str | None = None
        self.audit_bridge = AncileAuditBridge(self, "kamikaze_ram")

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
        self.create_subscription(String, "/effector/selected_plan", self._on_effector_plan, reliable_qos)

        self.status_pub = self.create_publisher(String, "/kamikaze_status", reliable_qos)
        self.result_pub = self.create_publisher(String, "/engagement_result", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)
        self.get_logger().info("kamikaze_ram_node initialized (simulation-only kinetic ram path)")

    def _require_deploy_gate(self) -> bool:
        return bool(self.get_parameter("require_simulate_only_deploy_cmd").value)

    def _require_double(self) -> bool:
        return bool(self.get_parameter("require_double_authorization").value)

    def _on_effector_plan(self, msg: String) -> None:
        try:
            plan = json.loads(msg.data)
            selected = plan.get("selected") or {}
            self.latest_effector_mode = str(selected.get("mode", ""))
        except json.JSONDecodeError:
            self.latest_effector_mode = None

    def _on_deploy_cmd(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        if not payload.get("simulate_only", False):
            self.get_logger().info("kamikaze: rejected deploy cmd (simulate_only required)")
            return
        self.simulate_only_deploy_registered = True
        ack = {
            "micro_id": str(self.get_parameter("micro_id").value),
            "state": "simulate_only_arm_ack",
            "payload_class": "kamikaze_ram_simulation",
        }
        self.status_pub.publish(String(data=json.dumps(ack)))
        self.audit_bridge.emit("kamikaze_deploy_cmd", ack, xai_text="Simulated kamikaze arm acknowledge; human gates still apply.")

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

        deploy_ok = (not self._require_deploy_gate()) or self.simulate_only_deploy_registered
        mode_ok = self.latest_effector_mode == "kamikaze_ram"
        release_authorized = bool(payload.get("release_authorized", False))

        kinetic_simulated = auth_path_ok(
            self.safety_open,
            self.launch_authorized,
            self.terminal_authorized,
            release_authorized,
            self._require_double(),
        ) and deploy_ok and mode_ok

        v_close_mps = 85.0
        closing_ke = 0.5 * 2.5 * v_close_mps**2  # stub mass kg * v^2
        status: Dict[str, Any] = {
            "micro_id": str(self.get_parameter("micro_id").value),
            "mothership_id": str(self.get_parameter("mothership_id").value),
            "track_id": payload.get("track_id", "unknown"),
            "engagement_id": payload.get("engagement_id", f"kz-{int(time.time())}"),
            "state": "terminal_ram_impact_simulated" if kinetic_simulated else "hold_monitor_only",
            "simulated_closing_speed_mps": v_close_mps if kinetic_simulated else 0.0,
            "effector_mode_match": mode_ok,
            "safety_gate_open": self.safety_open,
            "double_human_gate_satisfied": kinetic_simulated or False,
            "kinetic_energy_impact_j_est": closing_ke if kinetic_simulated else 0.0,
            "notes": "Direct collision simulation only; no explosive payload.",
        }
        result = {
            "engagement_id": status["engagement_id"],
            "micro_id": status["micro_id"],
            "outcome": "simulated_kinetic_ram_impact" if kinetic_simulated else "blocked_policy_gate",
            "authorized_path_verified": kinetic_simulated,
            "impact_geometry": "terminal_ram_pure_ke_sim",
        }

        self.status_pub.publish(String(data=json.dumps(status)))
        self.result_pub.publish(String(data=json.dumps(result)))
        self.audit_pub.publish(String(data=json.dumps({"event": "kamikaze_ram_engagement", "result": result})))
        self.audit_bridge.emit(
            "kamikaze_ram_engagement",
            result,
            xai_text="Kamikaze ram is gated last-resort kinetic simulation; requires effector plan mode, safety, and human authorizations.",
        )


def main() -> None:
    rclpy.init()
    node = KamikazeRamNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
