#!/usr/bin/env python3
"""Simulation: directional acoustic disruptor micro payload (no real hardware)."""

import json
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class AcousticDisruptorNode(Node):
    def __init__(self) -> None:
        super().__init__("acoustic_disruptor_node")
        self.declare_parameter("mothership_id", "mhs-001")
        self.declare_parameter("publish_hz", 0.5)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        mid = str(self.get_parameter("mothership_id").value)
        topic_id = mid.replace("/", "_").replace("-", "_")
        self.pub = self.create_publisher(String, f"/micro/acoustic_disruptor/{topic_id}/status", qos)
        hz = max(0.1, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / hz, self._tick)

    def _tick(self) -> None:
        mid = str(self.get_parameter("mothership_id").value)
        payload = {
            "payload_type": "acoustic_disruptor",
            "mothership_id": mid,
            "beam_az_deg_sim": 42.0,
            "safe_standoff_m_sim": 80.0,
            "threat_state": "idle_sim",
            "stamp": time.time(),
        }
        self.pub.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = AcousticDisruptorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
