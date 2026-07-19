#!/usr/bin/env python3
import json

import rclpy
from clearsky_os_interfaces.srv import QueryCopilot
from rclpy.node import Node
from std_msgs.msg import String

try:
    from clearsky_rule_guard import classify_text
except ImportError:  # pragma: no cover
    classify_text = None  # type: ignore[assignment]


def build_summary(query: str) -> str:
    return f"Stub copilot summary: {query[:120]}"


class CopilotNode(Node):
    def __init__(self) -> None:
        super().__init__("copilot_node")
        self.safety_open = False
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.audit_pub = self.create_publisher(String, "/audit/events", 20)
        self.create_service(QueryCopilot, "/copilot/query", self._on_query)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_query(self, request: QueryCopilot.Request, response: QueryCopilot.Response) -> QueryCopilot.Response:
        # TODO: plug in local model provider and policy-aware retrieval stack.
        blocked = not self.safety_open
        if classify_text is not None and request.query:
            blocked = blocked or classify_text(request.query).label == "block"
        response.blocked = blocked
        response.summary = "Blocked by safety guard." if blocked else build_summary(request.query)
        response.rationale = "safety_gate_or_clearsky_guard_block" if blocked else "template_backend_stub"
        self.audit_pub.publish(String(data=json.dumps({"event": "copilot_query", "blocked": blocked, "session_id": request.session_id})))
        return response


def main() -> None:
    rclpy.init()
    node = CopilotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
