#!/usr/bin/env python3
import json

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class HumanInterfaceNode(Node):
    def __init__(self) -> None:
        super().__init__("human_interface_node")
        self.declare_parameter("ack_topic", "/human_ack")
        self.declare_parameter("operator_auth_topic", "/operator/authorizations")
        self.declare_parameter("xai_request_topic", "/xai/request")
        self.declare_parameter("xai_topic", "/xai_explanation")
        self.declare_parameter("default_track_id", "fused-00001")
        self.declare_parameter("default_action", "jam")

        qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=20)
        self.ack_pub = self.create_publisher(String, self.get_parameter("ack_topic").value, qos)
        self.auth_pub = self.create_publisher(String, self.get_parameter("operator_auth_topic").value, qos)
        self.xai_req_pub = self.create_publisher(String, self.get_parameter("xai_request_topic").value, qos)
        self.create_subscription(String, self.get_parameter("xai_topic").value, self._on_xai, qos)

        self.timer = self.create_timer(2.0, self._trigger_once)
        self.triggered = False

    def _on_xai(self, msg: String) -> None:
        self.get_logger().info(f"XAI: {msg.data}")

    def _trigger_once(self) -> None:
        if self.triggered:
            return
        self.triggered = True

        req = String()
        req.data = json.dumps({"request": "Explain current recommendation"})
        self.xai_req_pub.publish(req)

        ack = String()
        ack.data = "ACKNOWLEDGED"
        self.ack_pub.publish(ack)

        track_id = str(self.get_parameter("default_track_id").value)
        action = str(self.get_parameter("default_action").value)
        auth = String()
        auth.data = json.dumps({"authorizations": [{"track_id": track_id, "action": action, "authorized": True}]})
        self.auth_pub.publish(auth)


def main() -> None:
    rclpy.init()
    node = HumanInterfaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
