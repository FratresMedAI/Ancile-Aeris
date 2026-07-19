#!/usr/bin/env python3
import json

import rclpy
from clearsky_os_integration import ClearSkyAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def formation_mode(threat_level: str) -> str:
    return "containment_screen" if threat_level in {"high", "critical"} else "monitor_perimeter"


class DefensiveSwarmCoordinatorNode(Node):
    def __init__(self) -> None:
        super().__init__("defensive_swarm_coordinator_node")
        self.safety_open = False
        self.audit_bridge = ClearSkyAuditBridge(self, "defensive_swarm_coordinator")
        self.create_subscription(String, "/swarm/intent_assessment", self._on_intent, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/defensive_swarm/coordination", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_intent(self, msg: String) -> None:
        # TODO: implement multi-agent cooperative planning and conflict resolution.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        threat_level = str(payload.get("severity", "low"))
        out = {
            "mode": formation_mode(threat_level),
            "threat_level": threat_level,
            "requires_human_authorization": True,
            "monitor_only": not self.safety_open,
        }
        self.pub.publish(String(data=json.dumps(out)))
        self.audit_bridge.emit(
            "defensive_swarm_coordination",
            out,
            xai_text="Friendly defensive swarm coordination remains recommendation-only and human-vetted.",
        )


def main() -> None:
    rclpy.init()
    node = DefensiveSwarmCoordinatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
