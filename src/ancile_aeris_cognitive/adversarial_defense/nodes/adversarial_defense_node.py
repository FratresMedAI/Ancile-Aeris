#!/usr/bin/env python3
import json
import statistics

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from ancile_rule_guard import classify_text
except ImportError:  # pragma: no cover
    classify_text = None  # type: ignore[assignment]


def anomaly_score(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return min(1.0, statistics.pstdev(values))


class AdversarialDefenseNode(Node):
    def __init__(self) -> None:
        super().__init__("adversarial_defense_node")
        self.safety_open = False
        self.create_subscription(String, "/sensor/raw", self._on_sensor, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.sensor_health_pub = self.create_publisher(String, "/sensor_health", 20)
        self.alert_pub = self.create_publisher(String, "/adversarial_alert", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_sensor(self, msg: String) -> None:
        # TODO: integrate robust multimodal spoof detector with calibrated model confidence.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        values = [float(v) for v in payload.get("samples", [0.0])]
        score = anomaly_score(values)
        text = str(payload.get("operator_text", ""))
        blocked = False
        if classify_text is not None and text:
            blocked = classify_text(text).label == "block"
        health = {"sensor_name": payload.get("sensor", "unknown"), "health_score": max(0.0, 1.0 - score), "spoof_suspected": score > 0.35 or blocked}
        alert = {"severity": "high" if health["spoof_suspected"] else "low", "monitor_only": not self.safety_open, "summary": "suspicious_pattern" if health["spoof_suspected"] else "nominal"}
        self.sensor_health_pub.publish(String(data=json.dumps(health)))
        self.alert_pub.publish(String(data=json.dumps(alert)))


def main() -> None:
    rclpy.init()
    node = AdversarialDefenseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
