#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class LidarNode(Node):
    def __init__(self) -> None:
        super().__init__("lidar_node")
        self.declare_parameter("publish_topic", "/sensor/lidar/points")
        self.declare_parameter("publish_hz", 10.0)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=10)
        self.pub = self.create_publisher(String, self.get_parameter("publish_topic").value, qos)

        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.05, 1.0 / hz), self._tick)
        self.seq = 0

    def _tick(self) -> None:
        self.seq += 1
        payload = {
            "frame_id": "lidar_frame",
            "scan_id": f"lidar-{self.seq:05d}",
            "detections": [{"x": 12.0, "y": 3.1, "z": 1.7, "confidence": 0.76}],
            "source": "lidar_sim",
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = LidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
