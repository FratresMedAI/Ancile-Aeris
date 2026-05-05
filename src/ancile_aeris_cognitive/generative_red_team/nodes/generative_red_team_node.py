#!/usr/bin/env python3
import json
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def sample_threat_family() -> str:
    return random.choice(["swarm_probe", "rf_spoofing", "sensor_blinding", "coordinated_intrusion"])


class GenerativeRedTeamNode(Node):
    def __init__(self) -> None:
        super().__init__("generative_red_team_node")
        self.safety_open = False
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/red_team/scenarios", 20)
        self.timer = self.create_timer(1.0, self._on_tick)
        self.counter = 0

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_tick(self) -> None:
        # TODO: integrate generative world models to synthesize future threat playbooks.
        self.counter += 1
        out = {
            "scenario_id": f"redteam-{self.counter:04d}",
            "threat_family": sample_threat_family(),
            "synthetic_prompt": "Simulated future threat for defensive stress testing only.",
            "severity": 0.6,
            "monitor_only": not self.safety_open,
        }
        self.pub.publish(String(data=json.dumps(out)))


def main() -> None:
    rclpy.init()
    node = GenerativeRedTeamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
