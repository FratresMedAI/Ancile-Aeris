#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class BlackSkyCoreNode(Node):
    def __init__(self) -> None:
        super().__init__("blacksky_core_node")
        self.declare_parameter("pid_threshold", 0.999)
        self.declare_parameter("raw_track_topic", "/raw_tracks")
        self.declare_parameter("human_ack_topic", "/human_ack")
        self.declare_parameter("validated_track_topic", "/validated_track")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.create_subscription(String, self.get_parameter("raw_track_topic").value, self._on_track, qos)
        self.create_subscription(String, self.get_parameter("human_ack_topic").value, self._on_human_ack, qos)
        self.validated_pub = self.create_publisher(String, self.get_parameter("validated_track_topic").value, qos)

        self.continue_processing = False
        self.get_logger().info("BlackSky core initialized with soldier-root gates")

    def _on_human_ack(self, msg: String) -> None:
        self.continue_processing = str(msg.data).strip().upper() == "ACKNOWLEDGED"

    def _on_track(self, msg: String) -> None:
        try:
            track = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid /raw_tracks payload")
            return

        confidence = float(track.get("confidence", 0.0))
        pid_threshold = float(self.get_parameter("pid_threshold").value)

        if self.continue_processing and confidence >= pid_threshold:
            out = String()
            out.data = json.dumps({"validated": True, "track": track})
            self.validated_pub.publish(out)
        else:
            self.get_logger().info("track gated by PID or missing human acknowledgment")


def main() -> None:
    rclpy.init()
    node = BlackSkyCoreNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
