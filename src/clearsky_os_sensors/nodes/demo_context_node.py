#!/usr/bin/env python3
"""Optional demo context publishers. Does NOT own /digital_twin/veto (twin does)."""

import json
import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DemoContextNode(Node):
    def __init__(self) -> None:
        super().__init__("demo_context_node")
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("enable_demo_iff", True)
        self.declare_parameter("enable_demo_lidar_sigint", True)
        # Twin veto is owned by digital_twin_node — only publish if explicitly forced
        self.declare_parameter("force_demo_twin_veto", False)

        self.lidar_pub = self.create_publisher(String, "/sensor/lidar/points", 20)
        self.sigint_pub = self.create_publisher(String, "/sensor/sigint/elint", 20)
        self.iff_pub = self.create_publisher(String, "/iff/status", 20)
        self.twin_pub = self.create_publisher(String, "/digital_twin/veto", 20)

        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.1, 1.0 / hz), self._tick)
        self.tick_count = 0
        self.get_logger().info(
            "demo_context_node initialized "
            f"(force_demo_twin_veto={bool(self.get_parameter('force_demo_twin_veto').value)})"
        )

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()

        if bool(self.get_parameter("enable_demo_lidar_sigint").value):
            # Honest stub confidence — labeled synthetic, not model-grade
            lidar_payload = {
                "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "lidar_frame"},
                "detections": [
                    {
                        "id": f"lid-{self.tick_count:05d}",
                        "range_m": 120.0 + (self.tick_count % 30),
                        "bearing_deg": 20.0,
                        "confidence": 0.55,
                        "synthetic": True,
                    }
                ],
            }
            sigint_payload = {
                "confidence": 0.5,
                "emitter_type": "uas_c2_link",
                "band": "S",
                "synthetic": True,
            }
            self.lidar_pub.publish(String(data=json.dumps(lidar_payload)))
            self.sigint_pub.publish(String(data=json.dumps(sigint_payload)))

        if bool(self.get_parameter("enable_demo_iff").value):
            # Default unknown/hostile-unknown for demo — not a real IFF decode
            iff_payload = {"friendly": False, "source": "demo_stub", "synthetic": True}
            self.iff_pub.publish(String(data=json.dumps(iff_payload)))

        if bool(self.get_parameter("force_demo_twin_veto").value) or os.environ.get(
            "CLEARSKY_FORCE_DEMO_TWIN_VETO", ""
        ).lower() in {"1", "true", "yes"}:
            twin_payload = {
                "veto": False,
                "risk": 0.1,
                "source": "demo_context_forced",
                "synthetic": True,
            }
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
