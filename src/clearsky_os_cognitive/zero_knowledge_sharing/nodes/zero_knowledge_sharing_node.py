#!/usr/bin/env python3
import json
import time

import rclpy
from clearsky_os_interfaces.srv import ShareThreatIntel
from clearsky_os_integration import ClearSkyAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def build_share_id(partner: str) -> str:
    return f"{partner}-{int(time.time())}"


class ZeroKnowledgeSharingNode(Node):
    def __init__(self) -> None:
        super().__init__("zero_knowledge_sharing_node")
        self.safety_open = False
        self.audit_bridge = ClearSkyAuditBridge(self, "zero_knowledge_sharing")
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/threat_intel/shares", 20)
        self.create_service(ShareThreatIntel, "/threat_intel/share", self._on_share)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_share(self, request: ShareThreatIntel.Request, response: ShareThreatIntel.Response) -> ShareThreatIntel.Response:
        # TODO: integrate privacy-preserving proofs and federated policy controls.
        accepted = self.safety_open and request.privacy_tier.lower() in {"zkp_stub", "sanitized", "fouo_safe"}
        response.accepted = accepted
        response.share_id = build_share_id(request.partner) if accepted else "rejected"
        response.reason = "accepted_stub" if accepted else "blocked_by_policy_or_safety"
        self.pub.publish(String(data=json.dumps({
            "share_id": response.share_id,
            "partner": request.partner,
            "summary": request.summary,
            "privacy_tier": request.privacy_tier,
            "approved": accepted,
        })))
        self.audit_bridge.emit(
            "threat_intel_share",
            {"partner": request.partner, "approved": accepted, "privacy_tier": request.privacy_tier},
            xai_text="Threat intel sharing decision evaluated safety gate and privacy tier policy.",
        )
        return response


def main() -> None:
    rclpy.init()
    node = ZeroKnowledgeSharingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
