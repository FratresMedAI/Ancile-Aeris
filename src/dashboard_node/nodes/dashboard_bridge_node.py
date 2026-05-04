#!/usr/bin/env python3
import json
import os
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class DashboardBridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("dashboard_bridge_node")

        self.declare_parameter("fused_tracks_topic", "/fused_tracks")
        self.declare_parameter("threats_topic", "/threats")
        self.declare_parameter("effector_topic", "/effector_commands")
        self.declare_parameter("audit_topic", "/audit/events")
        self.declare_parameter("resilience_topic", "/sensor/resilience_alerts")
        self.declare_parameter("dashboard_state_topic", "/dashboard/state")
        self.declare_parameter("publish_hz", 5.0)
        self.declare_parameter("state_file", "/tmp/counterdrone_dashboard_state.json")

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.tracks = deque(maxlen=100)
        self.threats = deque(maxlen=100)
        self.commands = deque(maxlen=100)
        self.audits = deque(maxlen=200)
        self.resilience_alerts = deque(maxlen=100)

        self.create_subscription(String, self.get_parameter("fused_tracks_topic").value, self._on_tracks, qos)
        self.create_subscription(String, self.get_parameter("threats_topic").value, self._on_threats, qos)
        self.create_subscription(String, self.get_parameter("effector_topic").value, self._on_commands, qos)
        self.create_subscription(String, self.get_parameter("audit_topic").value, self._on_audit, qos)
        self.create_subscription(String, self.get_parameter("resilience_topic").value, self._on_resilience, qos)

        self.publisher = self.create_publisher(String, self.get_parameter("dashboard_state_topic").value, qos)
        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.1, 1.0 / hz), self._tick)

        self.get_logger().info("dashboard_bridge_node initialized")

    def _safe_parse(self, text: str) -> dict | None:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid JSON payload for dashboard bridge")
            return None

    def _on_tracks(self, msg: String) -> None:
        payload = self._safe_parse(msg.data)
        if payload:
            self.tracks.append(payload)

    def _on_threats(self, msg: String) -> None:
        payload = self._safe_parse(msg.data)
        if payload:
            self.threats.append(payload)

    def _on_commands(self, msg: String) -> None:
        payload = self._safe_parse(msg.data)
        if payload:
            self.commands.append(payload)

    def _on_audit(self, msg: String) -> None:
        payload = self._safe_parse(msg.data)
        if payload:
            self.audits.append(payload)

    def _on_resilience(self, msg: String) -> None:
        payload = self._safe_parse(msg.data)
        if payload:
            self.resilience_alerts.append(payload)

    def _tick(self) -> None:
        state = {
            "summary": {
                "tracks": len(self.tracks),
                "threats": len(self.threats),
                "commands": len(self.commands),
                "audits": len(self.audits),
                "resilience_alerts": len(self.resilience_alerts),
            },
            "latest": {
                "track": self.tracks[-1] if self.tracks else {},
                "threat": self.threats[-1] if self.threats else {},
                "command": self.commands[-1] if self.commands else {},
                "audit": self.audits[-1] if self.audits else {},
                "resilience": self.resilience_alerts[-1] if self.resilience_alerts else {},
            },
        }
        msg = String()
        msg.data = json.dumps(state)
        self.publisher.publish(msg)

        state_file = str(self.get_parameter("state_file").value)
        os.makedirs(os.path.dirname(state_file), exist_ok=True)
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f)


def main() -> None:
    rclpy.init()
    node = DashboardBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
