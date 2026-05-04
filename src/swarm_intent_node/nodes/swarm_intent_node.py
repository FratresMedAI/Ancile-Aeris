#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def classify_swarm(tracks: list[dict]) -> str:
    if len(tracks) >= 6:
        return "saturation_attack"
    if len(tracks) >= 3:
        return "probe_cluster"
    return "single_or_scatter"


class SwarmIntentNode(Node):
    def __init__(self) -> None:
        super().__init__("swarm_intent_node")
        self.declare_parameter("fused_topic", "/fused_tracks")
        self.declare_parameter("predicted_topic", "/predicted_trajectories")
        self.declare_parameter("intent_topic", "/swarm/intent_assessment")
        self.declare_parameter("recommendations_topic", "/swarm/layered_recommendations")
        self.declare_parameter("publish_hz", 5.0)

        self.latest_tracks: list[dict] = []
        self.latest_predictions: list[dict] = []
        self.create_subscription(String, str(self.get_parameter("fused_topic").value), self._on_fused, 20)
        self.create_subscription(String, str(self.get_parameter("predicted_topic").value), self._on_predicted, 20)
        self.intent_pub = self.create_publisher(String, str(self.get_parameter("intent_topic").value), 20)
        self.recommendation_pub = self.create_publisher(
            String, str(self.get_parameter("recommendations_topic").value), 20
        )
        hz = float(self.get_parameter("publish_hz").value)
        self.create_timer(max(0.1, 1.0 / hz), self._tick)

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_tracks = payload.get("tracks", [])
        except json.JSONDecodeError:
            self.get_logger().warning("invalid fused payload for swarm intent")

    def _on_predicted(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.latest_predictions = payload.get("predictions", [])
        except json.JSONDecodeError:
            self.get_logger().warning("invalid predicted payload for swarm intent")

    def _layered_recommendations(self, intent: str) -> list[dict]:
        if intent == "saturation_attack":
            return [
                {"action": "jam", "sector": "wide", "priority": 1},
                {"action": "spoof", "sector": "decoy_corridor", "priority": 2},
            ]
        if intent == "probe_cluster":
            return [{"action": "monitor", "sector": "cluster_focus", "priority": 1}]
        return [{"action": "monitor", "sector": "single_track", "priority": 1}]

    def _tick(self) -> None:
        if not self.latest_tracks:
            return
        intent = classify_swarm(self.latest_tracks)
        intent_payload = {
            "intent": intent,
            "track_count": len(self.latest_tracks),
            "prediction_count": len(self.latest_predictions),
        }
        recommendations = self._layered_recommendations(intent)

        msg_intent = String()
        msg_intent.data = json.dumps(intent_payload)
        self.intent_pub.publish(msg_intent)

        msg_reco = String()
        msg_reco.data = json.dumps({"intent": intent, "recommendations": recommendations})
        self.recommendation_pub.publish(msg_reco)


def main() -> None:
    rclpy.init()
    node = SwarmIntentNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
