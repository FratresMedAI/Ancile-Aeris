#!/usr/bin/env python3
import json
import time

import rclpy
from ancile_aeris_interfaces.srv import RequestModelUpdate
from rclpy.node import Node
from std_msgs.msg import String


def build_update_id(model_name: str) -> str:
    return f"{model_name}-{int(time.time())}"


class FederatedLearningNode(Node):
    def __init__(self) -> None:
        super().__init__("federated_learning_node")
        self.safety_open = False
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.status_pub = self.create_publisher(String, "/federated_learning/status", 20)
        self.create_service(RequestModelUpdate, "/federated_learning/request_model_update", self._handle_update)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _handle_update(self, request: RequestModelUpdate.Request, response: RequestModelUpdate.Response) -> RequestModelUpdate.Response:
        # TODO: wire real privacy-preserving aggregation and signed model validation.
        accepted = self.safety_open and request.privacy_tier.lower() in {"dp", "secure_agg", "simulated"}
        response.accepted = accepted
        response.update_id = build_update_id(request.model_name) if accepted else "rejected"
        response.reason = "accepted_stub" if accepted else "blocked_by_safety_or_privacy"
        self.status_pub.publish(String(data=json.dumps({"event": "model_update_request", "accepted": accepted, "model": request.model_name})))
        return response


def main() -> None:
    rclpy.init()
    node = FederatedLearningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
