#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class HilTestNode(Node):
    def __init__(self) -> None:
        super().__init__("hil_test_node")
        self.declare_parameter("output_topic", "/hil/status")
        self.declare_parameter("publish_hz", 2.0)

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.pub = self.create_publisher(String, self.get_parameter("output_topic").value, qos)
        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.2, 1.0 / hz), self._tick)
        self.seq = 0

    def _tick(self) -> None:
        self.seq += 1
        msg = String()
        msg.data = json.dumps(
            {
                "test_id": f"hil-{self.seq:05d}",
                "camera_stub": "ready",
                "sdr_stub": "ready",
                "gpio_stub": "ready",
                "result": "pass",
            }
        )
        self.pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = HilTestNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
