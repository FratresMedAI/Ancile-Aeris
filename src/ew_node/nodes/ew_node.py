#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class EwNode(Node):
    def __init__(self) -> None:
        super().__init__("ew_node")
        self.declare_parameter("rf_topic", "/sensor/rf/detections")
        self.declare_parameter("sigint_topic", "/sensor/sigint/elint")
        self.declare_parameter("threats_topic", "/threats")
        self.declare_parameter("output_topic", "/ew/recommendations")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.create_subscription(String, self.get_parameter("rf_topic").value, self._on_rf, qos)
        self.create_subscription(String, self.get_parameter("sigint_topic").value, self._on_sigint, qos)
        self.create_subscription(String, self.get_parameter("threats_topic").value, self._on_threats, qos)
        self.pub = self.create_publisher(String, self.get_parameter("output_topic").value, qos)

        self.latest_rf = None
        self.latest_sigint = None
        self.latest_threat = None
        self.timer = self.create_timer(0.5, self._tick)

    def _on_rf(self, msg: String) -> None:
        try:
            self.latest_rf = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rf payload for ew_node")

    def _on_sigint(self, msg: String) -> None:
        try:
            self.latest_sigint = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid sigint payload for ew_node")

    def _on_threats(self, msg: String) -> None:
        try:
            self.latest_threat = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid threats payload for ew_node")

    def _tick(self) -> None:
        confidence = 0.0
        if self.latest_threat and self.latest_threat.get("threats"):
            confidence = float(self.latest_threat["threats"][0].get("score", 0.0))

        spectrum_anomaly = bool(self.latest_sigint and self.latest_sigint.get("signal_type") == "control_link_candidate")

        recommendation = {
            "mode": "cognitive_ew_defensive_sim",
            "spectrum_anomaly": spectrum_anomaly,
            "threat_score": confidence,
            "recommended_action": "monitor" if confidence < 0.7 else "prioritize_tracking_and_deconfliction",
        }

        msg = String()
        msg.data = json.dumps(recommendation)
        self.pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = EwNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
