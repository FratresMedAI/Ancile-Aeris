#!/usr/bin/env python3
import json
import time
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DarkspaceAuditNode(Node):
    def __init__(self) -> None:
        super().__init__("darkspace_audit_node")
        self.events_seen = 0
        self.integrity_ok = True
        self.chain_gap_count = 0
        self.last_event_hash_by_component: dict[str, str] = {}
        self.component_initialized: set[str] = set()
        self.recent_components: deque[str] = deque(maxlen=16)
        self.last_warning_time_by_component: dict[str, float] = {}
        self.multi_publisher_detected = False
        self.declare_parameter("mismatch_warning_cooldown_sec", 10.0)
        self.declare_parameter("max_expected_audit_publishers", 8)

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
        chain_id = str(payload.get("chain_id", ""))
        chain_key = f"{component}::{chain_id}" if chain_id else component
        self.recent_components.append(component)
        expected_previous = self.last_event_hash_by_component.get(chain_key, "GENESIS")

        # Startup/restart sync: if this component is first seen and already has
        # a non-GENESIS previous hash, adopt chain head without warning spam.
        bootstrap_sync = False
        if chain_key not in self.component_initialized:
            self.component_initialized.add(chain_key)
            bootstrap_sync = bool(previous_hash and expected_previous == "GENESIS" and previous_hash != "GENESIS")

        mismatch = bool(previous_hash and previous_hash != expected_previous and not bootstrap_sync)
        if mismatch:
            self.chain_gap_count += 1
            publisher_count = self.count_publishers("/audit/events")
            max_expected = int(self.get_parameter("max_expected_audit_publishers").value)
            cooldown = float(self.get_parameter("mismatch_warning_cooldown_sec").value)
            now = time.time()
            last_warn = self.last_warning_time_by_component.get(chain_key, 0.0)

            if publisher_count > max_expected:
                if not self.multi_publisher_detected:
                    self.multi_publisher_detected = True
                    self.get_logger().warning(
                        f"darkspace detected unusually high /audit/events publisher count ({publisher_count}); "
                        "concurrent stacks can interleave hash chains and trigger mismatch spam"
                    )
            elif now - last_warn >= cooldown:
                self.last_warning_time_by_component[chain_key] = now
                self.get_logger().info(
                    "darkspace audit continuity gap observed; adopting latest chain head"
                )

        if event_hash:
            self.last_event_hash_by_component[chain_key] = event_hash

    def _publish_status(self) -> None:
        body = {
            "integrity_ok": self.integrity_ok,
            "events_seen": self.events_seen,
            "chain_gap_count": self.chain_gap_count,
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
