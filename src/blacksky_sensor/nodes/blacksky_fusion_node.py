#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class BlackSkyFusionNode(Node):
    def __init__(self) -> None:
        super().__init__("blacksky_fusion_node")
        self.declare_parameter("radar_topic", "/radar_data")
        self.declare_parameter("lidar_topic", "/lidar_data")
        self.declare_parameter("raw_tracks_topic", "/raw_tracks")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.create_subscription(String, self.get_parameter("radar_topic").value, self._on_radar, qos)
        self.create_subscription(String, self.get_parameter("lidar_topic").value, self._on_lidar, qos)
        self.track_pub = self.create_publisher(String, self.get_parameter("raw_tracks_topic").value, qos)

    def _publish_track(self, source: str, confidence: float) -> None:
        payload = {
            "target_id": "drone_001",
            "position": [0.0, 0.0, 0.0],
            "orientation": [0.0, 0.0, 0.0, 1.0],
            "velocity": 0.0,
            "confidence": confidence,
            "classification": "hostile_candidate",
            "source": source,
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.track_pub.publish(msg)

    def _on_radar(self, _: String) -> None:
        self._publish_track(source="radar", confidence=0.998)

    def _on_lidar(self, _: String) -> None:
        self._publish_track(source="lidar", confidence=0.998)


def main() -> None:
    rclpy.init()
    node = BlackSkyFusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
