#!/usr/bin/env python3
import json
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def mismatch_score(visual_tracks: int, rf_hits: int, acoustic_hits: int) -> float:
    total_non_visual = rf_hits + acoustic_hits
    if visual_tracks == 0 and total_non_visual == 0:
        return 0.0
    if visual_tracks == 0:
        return 1.0
    return min(1.0, abs(visual_tracks - total_non_visual) / max(1, visual_tracks + total_non_visual))


class SensorResilienceNode(Node):
    def __init__(self) -> None:
        super().__init__("sensor_resilience_node")
        self.declare_parameter("visual_topic", "/sensor/visual/tracks")
        self.declare_parameter("rf_topic", "/sensor/rf/detections")
        self.declare_parameter("acoustic_topic", "/sensor/acoustic/detections")
        self.declare_parameter("alerts_topic", "/sensor/resilience_alerts")
        self.declare_parameter("publish_hz", 2.0)

        self.visual_count = 0
        self.rf_count = 0
        self.acoustic_count = 0
        self.alert_history = deque(maxlen=10)

        self.create_subscription(String, str(self.get_parameter("visual_topic").value), self._on_visual, 20)
        self.create_subscription(String, str(self.get_parameter("rf_topic").value), self._on_rf, 20)
        self.create_subscription(String, str(self.get_parameter("acoustic_topic").value), self._on_acoustic, 20)
        self.alert_pub = self.create_publisher(String, str(self.get_parameter("alerts_topic").value), 20)
        hz = float(self.get_parameter("publish_hz").value)
        self.create_timer(max(0.2, 1.0 / hz), self._tick)

    def _on_visual(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.visual_count = len(payload.get("tracks", []))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid visual payload for resilience")

    def _on_rf(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.rf_count = len(payload.get("fingerprints", []))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rf payload for resilience")

    def _on_acoustic(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.acoustic_count = len(payload.get("detections", []))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid acoustic payload for resilience")

    def _tick(self) -> None:
        score = mismatch_score(self.visual_count, self.rf_count, self.acoustic_count)
        if score < 0.5:
            return
        reasons = []
        if self.visual_count == 0 and (self.rf_count + self.acoustic_count) > 0:
            reasons.append("visual_degraded_or_occluded")
        if self.rf_count == 0 and self.visual_count > 0:
            reasons.append("rf_gap")
        if self.acoustic_count == 0 and self.visual_count > 0:
            reasons.append("acoustic_gap")
        alert = {
            "event": "sensor_resilience_alert",
            "mismatch_score": round(score, 4),
            "visual_tracks": self.visual_count,
            "rf_hits": self.rf_count,
            "acoustic_hits": self.acoustic_count,
            "reasons": reasons,
            "recommended_action": "monitor_and_rebalance_sensor_weighting",
        }
        self.alert_history.append(alert)
        msg = String()
        msg.data = json.dumps({"alerts": [alert], "history_depth": len(self.alert_history)})
        self.alert_pub.publish(msg)


def main() -> None:
    rclpy.init()
    node = SensorResilienceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
