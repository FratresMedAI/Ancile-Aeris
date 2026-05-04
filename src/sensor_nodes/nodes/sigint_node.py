#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class SigintNode(Node):
    def __init__(self) -> None:
        super().__init__("sigint_node")
        self.declare_parameter("publish_topic", "/sensor/sigint/elint")
        self.declare_parameter("publish_hz", 5.0)

        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=10)
        self.pub = self.create_publisher(String, self.get_parameter("publish_topic").value, qos)

        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.1, 1.0 / hz), self._tick)
        self.seq = 0

    def _tick(self) -> None:
        self.seq += 1
        payload = {
            "event_id": f"sigint-{self.seq:05d}",
            "band_hz": [2.4e9, 2.5e9],
            "signal_type": "control_link_candidate",
            "confidence": 0.74,
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = SigintNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
