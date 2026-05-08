#!/usr/bin/env python3
"""Simulation: micro sensor pod carried by mothership FOB (multi-modal ISR extension)."""

import json
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class SensorPodNode(Node):
    def __init__(self) -> None:
        super().__init__("sensor_pod_node")
        self.declare_parameter("mothership_id", "mhs-001")
        self.declare_parameter("publish_hz", 0.5)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        mid = str(self.get_parameter("mothership_id").value)
        topic_id = mid.replace("/", "_").replace("-", "_")
        topic = f"/micro/sensor_pod/{topic_id}/status"
        self.pub = self.create_publisher(String, topic, qos)
        hz = max(0.1, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / hz, self._tick)
        self.get_logger().info(f"sensor_pod_node sim on {topic}")

    def _tick(self) -> None:
        mid = str(self.get_parameter("mothership_id").value)
        payload = {
            "payload_type": "sensor_pod",
            "mothership_id": mid,
            "modalities_sim": ["eo_ir", "thermal", "rf_passive", "lidar_stub"],
            "coverage_extension_km2": 2.4,
            "sim_note": "ISR extension pod; simulation only.",
            "stamp": time.time(),
        }
        self.pub.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = SensorPodNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
