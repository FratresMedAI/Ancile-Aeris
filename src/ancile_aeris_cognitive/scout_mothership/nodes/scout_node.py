#!/usr/bin/env python3
import json
import time

import rclpy
from ancile_aeris_integration import AncileAuditBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


SCOUT_SOURCE = "scout_mothership"


def loiter_profile() -> dict:
    return {
        "altitude_m": 4500.0,
        "endurance_hr": 24.0,
        "sensors": ["eo_ir", "rf", "acoustic"],
    }


class ScoutMothershipNode(Node):
    def __init__(self) -> None:
        super().__init__("scout_mothership_node")
        self.declare_parameter("publish_hz", 1.0)
        self.declare_parameter("confidence", 0.92)

        self.safety_open = False
        self.launch_authorized = False
        self.track_idx = 0
        self.audit_bridge = AncileAuditBridge(self, SCOUT_SOURCE)

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(String, "/fused_tracks", self._on_fused, reliable_qos)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, reliable_qos)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, reliable_qos)
        self.fused_pub = self.create_publisher(String, "/fused_tracks", reliable_qos)
        self.scout_pub = self.create_publisher(String, "/scout_eyes", reliable_qos)
        self.handoff_pub = self.create_publisher(String, "/interceptor_handoff", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)

        publish_hz = max(0.2, float(self.get_parameter("publish_hz").value))
        self.timer = self.create_timer(1.0 / publish_hz, self._publish_scout_overlay)
        self.get_logger().info("scout_mothership_node initialized")

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

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        if payload.get("producer") == SCOUT_SOURCE:
            return

        tracks = payload.get("tracks", [])
        if not tracks:
            return

        first = tracks[0]
        scout_packet = self._scout_packet(
            track_id=str(first.get("track_id", "unknown")),
            x=float(first.get("x", 0.0)),
            y=float(first.get("y", 0.0)),
            confidence=float(first.get("confidence", 0.0)),
        )
        self.scout_pub.publish(String(data=json.dumps(scout_packet)))
        self._publish_handoff(scout_packet["track_id"])

    def _publish_scout_overlay(self) -> None:
        self.track_idx += 1
        profile = loiter_profile()
        x = 120.0 + (self.track_idx % 15) * 2.5
        y = 80.0 + (self.track_idx % 11) * 1.5
        confidence = float(self.get_parameter("confidence").value)
        now = self.get_clock().now().to_msg()
        track = {
            "track_id": f"scout-{self.track_idx:05d}",
            "x": x,
            "y": y,
            "vx": 2.5,
            "vy": 1.5,
            "altitude_m": profile["altitude_m"],
            "sensor_type": "high_altitude_eo_ir_rf",
            "confidence": confidence,
            "class_label": "scout_observed_uas_candidate",
            "source": SCOUT_SOURCE,
        }
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": SCOUT_SOURCE,
            "tracks": [track],
            "fusion": {
                "method": "high_altitude_isr_overlay_sim",
                "model": "scout_mothership_stub",
                "sources": profile["sensors"],
            },
            "pid": {
                "gate": 0.999,
                "confidence": confidence,
                "required_modalities": ["eo_ir", "rf"],
                "present_modalities": ["eo_ir", "rf", "acoustic"],
                "passed": False,
            },
        }
        self.fused_pub.publish(String(data=json.dumps(payload)))
        self.scout_pub.publish(String(data=json.dumps(self._scout_packet(track["track_id"], x, y, confidence))))

    def _scout_packet(self, track_id: str, x: float, y: float, confidence: float) -> dict:
        profile = loiter_profile()
        return {
            "track_id": track_id,
            "source": SCOUT_SOURCE,
            "x": x,
            "y": y,
            "altitude_m": profile["altitude_m"],
            "sensor_type": "high_altitude_eo_ir_rf",
            "confidence": confidence,
            "notes": "simulation_safe_high_altitude_isr",
        }

    def _publish_handoff(self, track_id: str) -> None:
        authorized_release = self.safety_open and self.launch_authorized
        handoff = {
            "engagement_id": f"handoff-{int(time.time())}",
            "track_id": track_id,
            "release_authorized": authorized_release,
            "requires_terminal_authorization": True,
            "monitor_only": not authorized_release,
        }
        self.handoff_pub.publish(String(data=json.dumps(handoff)))
        self.audit_pub.publish(String(data=json.dumps({"event": "scout_handoff", "handoff": handoff})))
        self.audit_bridge.emit(
            "scout_handoff",
            handoff,
            xai_text="Scout mothership generated simulation ISR handoff; interceptor release remains human gated.",
        )


def main() -> None:
    rclpy.init()
    node = ScoutMothershipNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
