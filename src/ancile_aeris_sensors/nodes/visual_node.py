#!/usr/bin/env python3
import json
import time
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class VisualTrack:
    track_id: str
    cls: str
    confidence: float
    x: float
    y: float
    w: float
    h: float
    source: str = "visual"


class VisualNode(Node):
    def __init__(self) -> None:
        super().__init__("visual_node")

        self.declare_parameter("model_name", "yolo26s")
        self.declare_parameter("weights_path", "models/visual/yolo26s.pt")
        self.declare_parameter("onnx_path", "models/visual/yolo26s.onnx")
        self.declare_parameter("engine_path", "models/visual/yolo26s.engine")
        self.declare_parameter("publish_topic", "/sensor/visual/tracks")
        self.declare_parameter("publish_fps", 15.0)
        self.declare_parameter("sim_mode", True)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        publish_topic = self.get_parameter("publish_topic").get_parameter_value().string_value
        self.publisher = self.create_publisher(String, publish_topic, qos)

        fps = self.get_parameter("publish_fps").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.01, 1.0 / fps), self._tick)

        self.frame_idx = 0
        self.get_logger().info("visual_node initialized (YOLO26 integration stub active)")

    def _tick(self) -> None:
        self.frame_idx += 1
        now = self.get_clock().now().to_msg()
        tsec = time.time()

        simulated_track = VisualTrack(
            track_id=f"vis-{self.frame_idx:05d}",
            cls="drone",
            confidence=0.88,
            x=0.4 + 0.1 * (self.frame_idx % 5) / 5.0,
            y=0.35,
            w=0.12,
            h=0.08,
        )

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "camera_optical_frame",
            },
            "model": {
                "name": self.get_parameter("model_name").value,
                "backend": "onnx_or_tensorrt",
            },
            "latency_ms": 20.0,
            "tracks": [asdict(simulated_track)],
            "runtime": {"unix_time": tsec},
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = VisualNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
