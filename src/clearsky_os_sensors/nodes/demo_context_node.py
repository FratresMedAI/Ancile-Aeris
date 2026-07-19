#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DemoContextNode(Node):
    def __init__(self) -> None:
        super().__init__("demo_context_node")
        self.declare_parameter("publish_hz", 10.0)

        self.lidar_pub = self.create_publisher(String, "/sensor/lidar/points", 20)
        self.sigint_pub = self.create_publisher(String, "/sensor/sigint/elint", 20)
        self.iff_pub = self.create_publisher(String, "/iff/status", 20)
        self.twin_pub = self.create_publisher(String, "/digital_twin/veto", 20)

        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.1, 1.0 / hz), self._tick)
        self.tick_count = 0
        self.get_logger().info("demo_context_node initialized")

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()

        lidar_payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "lidar_frame"},
            "detections": [
                {"id": f"lid-{self.tick_count:05d}", "range_m": 412.0, "bearing_deg": 34.0, "confidence": 0.999}
            ],
        }
        sigint_payload = {"confidence": 0.999, "emitter_type": "uas_c2_link", "band": "S"}
        iff_payload = {"friendly": False}
        twin_payload = {"veto": False, "risk": 0.08}

        self.lidar_pub.publish(String(data=json.dumps(lidar_payload)))
        self.sigint_pub.publish(String(data=json.dumps(sigint_payload)))
        self.iff_pub.publish(String(data=json.dumps(iff_payload)))
        self.twin_pub.publish(String(data=json.dumps(twin_payload)))


def main() -> None:
    rclpy.init()
    node = DemoContextNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
