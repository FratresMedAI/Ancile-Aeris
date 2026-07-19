#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def cluster_size_to_intent(cluster_size: int) -> str:
    if cluster_size >= 6:
        return "coordinated_swarm"
    if cluster_size >= 3:
        return "probing_group"
    return "single_actor"


class SwarmOrchestratorNode(Node):
    def __init__(self) -> None:
        super().__init__("swarm_orchestrator_node")
        self.safety_open = False
        self.create_subscription(String, "/fused_tracks", self._on_tracks, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.intent_pub = self.create_publisher(String, "/swarm/intent_assessment", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_tracks(self, msg: String) -> None:
        # TODO: replace with robust clustering and trajectory manifold reasoning.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks", [])
        intent = cluster_size_to_intent(len(tracks))
        out = {"intent": intent, "cluster_size": len(tracks), "monitor_only": not self.safety_open}
        self.intent_pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = SwarmOrchestratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
