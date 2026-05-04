#!/usr/bin/env python3
import json
import math
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class SimThreat:
    track_id: str
    x: float
    y: float
    vx: float
    vy: float
    confidence: float


@dataclass
class RlRecommendation:
    track_id: str
    preferred_action: str
    policy_id: str
    confidence: float


class SwarmSimNode(Node):
    def __init__(self) -> None:
        super().__init__("swarm_sim_node")

        self.declare_parameter("sim_mode", True)
        self.declare_parameter("sim_hz", 10.0)
        self.declare_parameter("sim_tracks_topic", "/sim/swarm_tracks")
        self.declare_parameter("rl_recommendation_topic", "/sim/rl_recommendations")
        self.declare_parameter("policy_id", "ppo_multiagent_stub_v1")

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.tracks_pub = self.create_publisher(String, self.get_parameter("sim_tracks_topic").value, qos)
        self.rl_pub = self.create_publisher(String, self.get_parameter("rl_recommendation_topic").value, qos)

        hz = float(self.get_parameter("sim_hz").value)
        self.timer = self.create_timer(max(0.05, 1.0 / hz), self._tick)
        self.k = 0
        self.get_logger().info("swarm_sim_node initialized")

    def _tick(self) -> None:
        if not bool(self.get_parameter("sim_mode").value):
            return

        self.k += 1
        t = self.k * 0.1

        threats: list[SimThreat] = []
        recs: list[RlRecommendation] = []
        for i in range(3):
            x = 100.0 + 20.0 * i + 5.0 * math.cos(t + i)
            y = 50.0 + 10.0 * i + 5.0 * math.sin(t + i)
            vx = -2.0 - 0.2 * i
            vy = -1.0
            track_id = f"sim-track-{i+1:02d}"
            conf = 0.80 + 0.03 * i
            threats.append(SimThreat(track_id=track_id, x=x, y=y, vx=vx, vy=vy, confidence=conf))

            action = "jam" if i == 0 else "spoof"
            recs.append(
                RlRecommendation(
                    track_id=track_id,
                    preferred_action=action,
                    policy_id=str(self.get_parameter("policy_id").value),
                    confidence=0.70 + 0.1 * i,
                )
            )

        tracks_msg = String()
        tracks_msg.data = json.dumps({"sim_tracks": [asdict(t) for t in threats]})
        self.tracks_pub.publish(tracks_msg)

        rl_msg = String()
        rl_msg.data = json.dumps({"recommendations": [asdict(r) for r in recs]})
        self.rl_pub.publish(rl_msg)


def main() -> None:
    rclpy.init()
    node = SwarmSimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
