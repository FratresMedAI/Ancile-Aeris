#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def classify_behavior(speed: float, turn_rate: float) -> str:
    if speed < 2.0:
        return "loiter"
    if turn_rate > 0.7:
        return "evasive"
    return "approach"


class VideoAnalyticsNode(Node):
    def __init__(self) -> None:
        super().__init__("video_analytics_node_v2")
        self.safety_open = False
        self.create_subscription(String, "/camera/tracks", self._on_track, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/sensor/visual/analytics", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_track(self, msg: String) -> None:
        # TODO: connect detector backend (YOLO/RT-DETR) and tracking ID association.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        speed = float(payload.get("speed", 0.0))
        turn_rate = float(payload.get("turn_rate", 0.0))
        behavior = classify_behavior(speed, turn_rate)
        out = {"track_id": payload.get("track_id", "unknown"), "behavior": behavior, "monitor_only": not self.safety_open}
        self.pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = VideoAnalyticsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
