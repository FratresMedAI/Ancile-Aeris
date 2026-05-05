#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def integrity_state(gps_health: float) -> str:
    if gps_health < 0.3:
        return "denied_fallback_inertial"
    if gps_health < 0.6:
        return "degraded_blended"
    return "nominal_gnss"


class ResilientPntNode(Node):
    def __init__(self) -> None:
        super().__init__("resilient_pnt_node")
        self.safety_open = False
        self.create_subscription(String, "/sensor/pnt_status", self._on_pnt_status, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/navigation/resilient_pnt", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_pnt_status(self, msg: String) -> None:
        # TODO: add quantum-resistant timing and anti-spoof fusion across modalities.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        health = float(payload.get("gps_health", 0.0))
        out = {
            "source_mode": "inertial_visual_fallback_stub",
            "latitude": float(payload.get("latitude", 0.0)),
            "longitude": float(payload.get("longitude", 0.0)),
            "uncertainty_m": max(1.0, 50.0 * (1.0 - health)),
            "integrity_state": integrity_state(health),
            "monitor_only": not self.safety_open,
        }
        self.pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = ResilientPntNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
