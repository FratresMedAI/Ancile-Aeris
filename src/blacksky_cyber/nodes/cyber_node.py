#!/usr/bin/env python3
import hashlib
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class BlackSkyCyberNode(Node):
    def __init__(self) -> None:
        super().__init__("blacksky_cyber_node")
        self.declare_parameter("validated_track_topic", "/validated_track")
        self.declare_parameter("audit_topic", "/audit/events")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.create_subscription(String, self.get_parameter("validated_track_topic").value, self._on_track, qos)
        self.audit_pub = self.create_publisher(String, self.get_parameter("audit_topic").value, qos)
        self.last_hash = "genesis"

    def _on_track(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid /validated_track payload")
            return

        track = payload.get("track", {})
        entry = {
            "event": "validated_track_audit",
            "timestamp_ns": int(self.get_clock().now().nanoseconds),
            "target_id": track.get("target_id", "unknown"),
            "confidence": float(track.get("confidence", 0.0)),
            "source": track.get("source", "unknown"),
            "prev_hash": self.last_hash,
        }
        digest = hashlib.sha256(json.dumps(entry, sort_keys=True).encode("utf-8")).hexdigest()
        entry["hash"] = digest
        self.last_hash = digest

        out = String()
        out.data = json.dumps(entry)
        self.audit_pub.publish(out)


def main() -> None:
    rclpy.init()
    node = BlackSkyCyberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
