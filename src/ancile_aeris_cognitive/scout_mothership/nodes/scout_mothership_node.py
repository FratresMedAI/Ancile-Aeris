#!/usr/bin/env python3
import json
import time

import rclpy
from ancile_aeris_integration import AncileAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def loiter_profile() -> dict:
    return {"altitude_m": 4500.0, "endurance_hr": 24.0, "sensors": ["eo_ir", "rf", "acoustic"]}


class ScoutMothershipNode(Node):
    def __init__(self) -> None:
        super().__init__("scout_mothership_node")
        self.safety_open = False
        self.launch_authorized = False
        self.audit_bridge = AncileAuditBridge(self, "scout_mothership")
        self.create_subscription(String, "/fused_tracks", self._on_fused, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, 20)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, 20)
        self.scout_pub = self.create_publisher(String, "/scout_eyes", 20)
        self.handoff_pub = self.create_publisher(String, "/interceptor_handoff", 20)
        self.audit_pub = self.create_publisher(String, "/audit/events", 20)

    def _on_safety(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_launch_auth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        self.launch_authorized = bool(payload.get("approved", False))

    def _on_fused(self, msg: String) -> None:
        # TODO: integrate persistent high-altitude ISR planner and release logistics.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks", [])
        if not tracks:
            return
        first = tracks[0]
        scout_packet = {
            "track_id": first.get("track_id", "unknown"),
            "source": "scout_mothership",
            "confidence": float(first.get("confidence", 0.0)),
            "altitude_m": loiter_profile()["altitude_m"],
            "notes": "high_altitude_isr_stub",
        }
        self.scout_pub.publish(String(data=json.dumps(scout_packet)))
        authorized_release = self.safety_open and self.launch_authorized
        handoff = {
            "engagement_id": f"handoff-{int(time.time())}",
            "track_id": scout_packet["track_id"],
            "release_authorized": authorized_release,
            "requires_terminal_authorization": True,
            "monitor_only": not authorized_release,
        }
        self.handoff_pub.publish(String(data=json.dumps(handoff)))
        self.audit_pub.publish(String(data=json.dumps({"event": "scout_handoff", "handoff": handoff})))
        self.audit_bridge.emit(
            "scout_handoff",
            handoff,
            xai_text="Scout mothership produced high-altitude ISR handoff with human launch authorization checks.",
        )


def main() -> None:
    rclpy.init()
    node = ScoutMothershipNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
