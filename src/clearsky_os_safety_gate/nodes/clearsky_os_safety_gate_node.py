#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import rclpy
from clearsky_os_integration.helpers import ClearSkyAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


class ClearSkyOSSafetyGateNode(Node):
    def __init__(self) -> None:
        super().__init__("clearsky_os_safety_gate_node")
        self.declare_parameter("pid_target", 0.999)
        self.declare_parameter("publish_hz", 10.0)

        self.latest_track: dict = {}
        self.latest_operator: dict = {"human_veto": False, "approved": False, "terminal_approved": False}
        self.latest_iff: dict = {"friendly": False}
        self.latest_twin: dict = {"veto": False, "risk": 0.0}
        self.guard = self._load_guard()
        self.audit_bridge = ClearSkyAuditBridge(self, "clearsky_os_safety_gate_node")

        self.create_subscription(String, "/fused_tracks", self._on_fused_tracks, 20)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, 20)
        self.create_subscription(String, "/operator/terminal_authorizations", self._on_terminal_auth, 20)
        self.create_subscription(String, "/operator/veto", self._on_veto, 20)
        self.create_subscription(String, "/iff/status", self._on_iff_status, 20)
        self.create_subscription(String, "/digital_twin/veto", self._on_twin_veto, 20)

        self.status_pub = self.create_publisher(String, "/safety_gate_status", 20)
        hz = float(self.get_parameter("publish_hz").value)
        self.create_timer(max(0.1, 1.0 / hz), self._tick)

    def _load_guard(self):
        repo_root = Path(__file__).resolve().parents[3]
        guard_path = repo_root / "payloads" / "generic"
        if str(guard_path) not in sys.path:
            sys.path.insert(0, str(guard_path))
        try:
            from clearsky_rule_guard import classify_text  # type: ignore
            return classify_text
        except Exception:
            return None

    def _on_fused_tracks(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks", [])
        if tracks:
            self.latest_track = tracks[0]

    def _on_launch_auth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_operator["approved"] = bool(payload.get("approved", False))
        except json.JSONDecodeError:
            pass

    def _on_terminal_auth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_operator["terminal_approved"] = bool(payload.get("approved", False))
        except json.JSONDecodeError:
            pass

    def _on_veto(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_operator["human_veto"] = bool(payload.get("veto", False))
        except json.JSONDecodeError:
            pass

    def _on_iff_status(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_iff["friendly"] = bool(payload.get("friendly", False))
        except json.JSONDecodeError:
            pass

    def _on_twin_veto(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_twin["veto"] = bool(payload.get("veto", False))
            self.latest_twin["risk"] = float(payload.get("risk", 0.0))
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

    def _tick(self) -> None:
        confidence = float(self.latest_track.get("confidence", 0.0)) if self.latest_track else 0.0
        pid_target = float(self.get_parameter("pid_target").value)
        reasons = []
        allow = True

        if confidence < 0.6:
            allow = False
            reasons.append("low_fusion_confidence")
        if confidence < pid_target:
            allow = False
            reasons.append("pid_below_threshold")
        if bool(self.latest_operator.get("human_veto", False)):
            allow = False
            reasons.append("human_veto")
        if bool(self.latest_iff.get("friendly", False)):
            allow = False
            reasons.append("friendly_iff_lockout")
        if bool(self.latest_twin.get("veto", False)) or float(self.latest_twin.get("risk", 0.0)) > 0.7:
            allow = False
            reasons.append("digital_twin_veto")

        guard_block = False
        if self.guard is not None:
            text = json.dumps(self.latest_track) if self.latest_track else ""
            if text:
                guard_block = self.guard(text).label == "block"
        if guard_block:
            allow = False
            reasons.append("clearsky_rule_guard_block")

        out = {
            "allow": allow,
            "reasons": reasons,
            "pid_target": pid_target,
            "fused_confidence": confidence,
            "launch_authorized": bool(self.latest_operator.get("approved", False)),
            "terminal_authorized": bool(self.latest_operator.get("terminal_approved", False)),
            "friendly_iff": bool(self.latest_iff.get("friendly", False)),
            "digital_twin_veto": bool(self.latest_twin.get("veto", False)),
            "digital_twin_risk": float(self.latest_twin.get("risk", 0.0)),
        }
        self.status_pub.publish(String(data=json.dumps(out)))
        self.audit_bridge.emit(
            "safety_gate_evaluation",
            {"allow": allow, "reasons": reasons, "fused_confidence": confidence},
            xai_text=f"Safety gate {'allowed' if allow else 'blocked'} action.",
        )


def main() -> None:
    rclpy.init()
    node = ClearSkyOSSafetyGateNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
