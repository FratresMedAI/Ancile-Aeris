#!/usr/bin/env python3
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class RfFingerprint:
    emitter_id: str
    confidence: float
    center_freq_hz: float
    bandwidth_hz: float
    modulation_guess: str
    source: str = "rf"


class RfNode(Node):
    def __init__(self) -> None:
        super().__init__("rf_node")

        self.declare_parameter("model_name", "drone_rf_cnn")
        self.declare_parameter("publish_topic", "/sensor/rf/detections")
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("sim_mode", True)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        publish_topic = self.get_parameter("publish_topic").get_parameter_value().string_value
        self.publisher = self.create_publisher(String, publish_topic, qos)

        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.05, 1.0 / publish_hz), self._tick)
        self.tick_count = 0

        self.get_logger().info("rf_node initialized (GNU Radio + classifier stub active)")

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()

        fingerprint = RfFingerprint(
            emitter_id=f"rf-{self.tick_count:05d}",
            confidence=0.999,
            center_freq_hz=2.437e9,
            bandwidth_hz=20.0e6,
            modulation_guess="ofdm",
        )

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "rf_sensor_frame",
            },
            "model": self.get_parameter("model_name").value,
            "fingerprints": [asdict(fingerprint)],
            "latency_ms": 18.0,
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = RfNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
