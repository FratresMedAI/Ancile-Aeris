#!/usr/bin/env python3
import json
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def build_event(sensor_id: str, counter: int) -> dict:
    return {
        "event_id": f"{sensor_id}-{counter}",
        "sensor_id": sensor_id,
        "pixel_x": counter % 128,
        "pixel_y": (counter * 3) % 128,
        "polarity": 1.0 if counter % 2 else -1.0,
        "confidence": 0.6,
    }


class NeuromorphicSimNode(Node):
    def __init__(self) -> None:
        super().__init__("neuromorphic_sim_node")
        self.safety_open = False
        self.counter = 0
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/neuromorphic_events", 20)
        self.timer = self.create_timer(0.2, self._on_tick)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_tick(self) -> None:
        # TODO: plug in event-camera stream simulator and neuromorphic kernels.
        self.counter += 1
        event = build_event("neuromorphic_cam_stub", self.counter)
        event["timestamp"] = time.time()
        event["monitor_only"] = not self.safety_open
        self.pub.publish(String(data=json.dumps(event)))


def main() -> None:
    rclpy.init()
    node = NeuromorphicSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
