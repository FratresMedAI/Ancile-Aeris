#!/usr/bin/env python3
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class DigitalTwinState:
    scenario_id: str
    mirrored_tracks: int
    predicted_collisions: int
    soldier_risk: float
    confidence: float


class DigitalTwinNode(Node):
    def __init__(self) -> None:
        super().__init__("digital_twin_node")
        self.declare_parameter("fused_topic", "/fused_tracks")
        self.declare_parameter("output_topic", "/digital_twin_state")
        self.declare_parameter("publish_hz", 5.0)

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.create_subscription(String, self.get_parameter("fused_topic").value, self._on_fused, qos)
        self.pub = self.create_publisher(String, self.get_parameter("output_topic").value, qos)

        self.mirrored_tracks = 0
        hz = float(self.get_parameter("publish_hz").value)
        self.timer = self.create_timer(max(0.1, 1.0 / hz), self._tick)

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.mirrored_tracks = len(payload.get("tracks", []))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid fused payload for digital twin")

    def _tick(self) -> None:
        state = DigitalTwinState(
            scenario_id="sim-mirror-001",
            mirrored_tracks=self.mirrored_tracks,
            predicted_collisions=1 if self.mirrored_tracks > 0 else 0,
            soldier_risk=0.6 if self.mirrored_tracks > 0 else 0.0,
            confidence=0.8,
        )
        msg = String()
        msg.data = json.dumps({"digital_twin_state": asdict(state)})
        self.pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = DigitalTwinNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
