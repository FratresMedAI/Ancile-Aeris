#!/usr/bin/env python3
import json
from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


@dataclass
class AgentScore:
    detection: float
    intent: float
    mitigation: float
    safety: float


def aggregate_agent_score(score: AgentScore) -> float:
    return (score.detection + score.intent + score.mitigation + score.safety) / 4.0


class AgentOrchestratorNode(Node):
    def __init__(self) -> None:
        super().__init__("agent_orchestrator_node")
        self.safety_open = False
        self.create_subscription(String, "/fused_tracks", self._on_fused_tracks, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.proposed_pub = self.create_publisher(String, "/proposed_actions", 20)
        self.audit_pub = self.create_publisher(String, "/audit/events", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.safety_open = False
            return
        self.safety_open = bool(payload.get("allow", False))

    def _on_fused_tracks(self, msg: String) -> None:
        # TODO: replace with BT/LangGraph multi-agent coordination.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks", [])
        if not tracks:
            return
        track = tracks[0]
        score = aggregate_agent_score(AgentScore(0.6, 0.6, 0.55, 0.9 if self.safety_open else 0.2))
        action = "monitor" if (not self.safety_open or score < 0.7) else "jam_candidate"
        out = {"proposal_id": f"ao-{track.get('id', 'unknown')}", "track_id": track.get("id", "unknown"), "action": action, "score": score}
        self.proposed_pub.publish(String(data=json.dumps(out)))
        self.audit_pub.publish(String(data=json.dumps({"event": "agent_orchestrator_proposal", "proposal": out})))


def main() -> None:
    rclpy.init()
    node = AgentOrchestratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
