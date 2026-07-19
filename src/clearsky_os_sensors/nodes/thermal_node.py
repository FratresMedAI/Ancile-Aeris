#!/usr/bin/env python3
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class ThermalTrack:
    track_id: str
    cls: str
    confidence: float
    x: float
    y: float
    w: float
    h: float
    source: str = "thermal"


class ThermalNode(Node):
    def __init__(self) -> None:
        super().__init__("thermal_node")

        self.declare_parameter("model_name", "thermal_detector_stub")
        self.declare_parameter("publish_topic", "/sensor/thermal/tracks")
        self.declare_parameter("publish_hz", 10.0)

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
        self.get_logger().info("thermal_node initialized (simulation stub active)")

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()

        trk = ThermalTrack(
            track_id=f"thr-{self.tick_count:05d}",
            cls="drone_heat_signature",
            confidence=0.55,  # synthetic stub — not model inference
            x=0.42,
            y=0.34,
            w=0.11,
            h=0.07,
        )

        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "thermal_optical_frame"},
            "model": self.get_parameter("model_name").value,
            "tracks": [asdict(trk)],
            "latency_ms": 17.0,
        }

        self.publisher.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = ThermalNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
