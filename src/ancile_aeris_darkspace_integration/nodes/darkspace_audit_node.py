#!/usr/bin/env python3
import json
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DarkspaceAuditNode(Node):
    def __init__(self) -> None:
        super().__init__("darkspace_audit_node")
        self.events_seen = 0
        self.integrity_ok = True
        self.last_event_hash_by_component: dict[str, str] = {}
        self.recent_components: deque[str] = deque(maxlen=16)

        self.create_subscription(String, "/audit/events", self._on_audit_event, 50)
        self.status_pub = self.create_publisher(String, "/darkspace/status", 20)
        self.create_timer(1.0, self._publish_status)
        self.get_logger().info("darkspace_audit_node initialized")

    def _on_audit_event(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.integrity_ok = False
            self.get_logger().warning("invalid audit event payload")
            return

        self.events_seen += 1
        previous_hash = str(payload.get("previous_hash", ""))
        event_hash = str(payload.get("event_hash", ""))
        component = str(payload.get("component", "unknown"))
        self.recent_components.append(component)
        expected_previous = self.last_event_hash_by_component.get(component, "GENESIS")

        if previous_hash and previous_hash != expected_previous:
            self.integrity_ok = False
            self.get_logger().warning("darkspace hash-chain mismatch observed")

        if event_hash:
            self.last_event_hash_by_component[component] = event_hash

    def _publish_status(self) -> None:
        body = {
            "integrity_ok": self.integrity_ok,
            "events_seen": self.events_seen,
            "last_event_hashes": self.last_event_hash_by_component,
            "recent_components": list(self.recent_components),
        }
        self.status_pub.publish(String(data=json.dumps(body)))


def main() -> None:
    rclpy.init()
    node = DarkspaceAuditNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
