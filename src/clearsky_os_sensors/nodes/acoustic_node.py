#!/usr/bin/env python3
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class AcousticDetection:
    detection_id: str
    confidence: float
    estimated_bearing_deg: float
    frequency_band_hz: list[float]
    source: str = "acoustic"


class AcousticNode(Node):
    def __init__(self) -> None:
        super().__init__("acoustic_node")

        self.declare_parameter("model_name", "crnn_melspec")
        self.declare_parameter("publish_topic", "/sensor/acoustic/detections")
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
        self.get_logger().info("acoustic_node initialized (synthetic stub; CRNN Phase 2)")

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()

        det = AcousticDetection(
            detection_id=f"aud-{self.tick_count:05d}",
            confidence=0.55,  # synthetic stub — not model inference
            estimated_bearing_deg=35.0,
            frequency_band_hz=[120.0, 1800.0],
        )

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "mic_array_frame",
            },
            "model": self.get_parameter("model_name").value,
            "detections": [asdict(det)],
            "latency_ms": 15.0,
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = AcousticNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
