#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AncileAerisSafetyGateNode(Node):
    def __init__(self) -> None:
        super().__init__("ancile_aeris_safety_gate_node")
        self.declare_parameter("pid_target", 0.999)
        self.declare_parameter("publish_hz", 10.0)

        self.latest_track: dict = {}
        self.latest_operator: dict = {"human_veto": False, "approved": False, "terminal_approved": False}
        self.guard = self._load_guard()

        self.create_subscription(String, "/fused_tracks", self._on_fused_tracks, 20)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, 20)
        self.create_subscription(String, "/operator/terminal_authorizations", self._on_terminal_auth, 20)
        self.create_subscription(String, "/operator/veto", self._on_veto, 20)

        self.status_pub = self.create_publisher(String, "/safety_gate_status", 20)
        hz = float(self.get_parameter("publish_hz").value)
        self.create_timer(max(0.1, 1.0 / hz), self._tick)

    def _load_guard(self):
        repo_root = Path(__file__).resolve().parents[3]
        guard_path = repo_root / "payloads" / "generic"
        if str(guard_path) not in sys.path:
            sys.path.insert(0, str(guard_path))
        try:
            from ancile_rule_guard import classify_text  # type: ignore
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

        guard_block = False
        if self.guard is not None:
            text = json.dumps(self.latest_track) if self.latest_track else ""
            if text:
                guard_block = self.guard(text).label == "block"
        if guard_block:
            allow = False
            reasons.append("ancile_rule_guard_block")

        out = {
            "allow": allow,
            "reasons": reasons,
            "pid_target": pid_target,
            "fused_confidence": confidence,
            "launch_authorized": bool(self.latest_operator.get("approved", False)),
            "terminal_authorized": bool(self.latest_operator.get("terminal_approved", False)),
        }
        self.status_pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = AncileAerisSafetyGateNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
