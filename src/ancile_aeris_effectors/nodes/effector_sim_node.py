#!/usr/bin/env python3
"""Ancile Aeris effector health/state simulation publisher.

Publishes low-rate readiness telemetry for each non-kinetic effector mode
so demos can visualize layered availability without any real actuation.
"""

from __future__ import annotations

import json
from typing import Dict

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


EFFECTOR_HEALTH: Dict[str, Dict[str, float]] = {
    "hpm_denial_stub": {"readiness": 0.92, "duty_cycle": 0.18},
    "cognitive_jamming": {"readiness": 0.97, "duty_cycle": 0.42},
    "gnss_link_spoofing": {"readiness": 0.88, "duty_cycle": 0.10},
    "control_link_takeover": {"readiness": 0.74, "duty_cycle": 0.04},
    "multi_sensor_deception": {"readiness": 0.95, "duty_cycle": 0.31},
}


class EffectorSimNode(Node):
    def __init__(self) -> None:
        super().__init__("effector_sim_node")
        self.declare_parameter("publish_hz", 0.5)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.pub = self.create_publisher(String, "/effector/status", qos)
        publish_hz = max(0.1, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / publish_hz, self._tick)
        self.get_logger().info("effector_sim_node initialized (readiness telemetry only)")

    def _tick(self) -> None:
        now = self.get_clock().now().to_msg()
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": "ancile_aeris_effectors",
            "monitor_only": True,
            "modes": EFFECTOR_HEALTH,
        }
        self.pub.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = EffectorSimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
