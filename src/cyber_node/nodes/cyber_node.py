#!/usr/bin/env python3
import hashlib
import json
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class IdentityAssessment:
    emitter_id: str
    mac_oui: str
    vendor_guess: str
    rf_fingerprint_family: str
    disposition: str
    confidence: float


class CyberNode(Node):
    def __init__(self) -> None:
        super().__init__("cyber_node")

        self.declare_parameter("rf_topic", "/sensor/rf/detections")
        self.declare_parameter("output_topic", "/cyber/identity_assessments")
        self.declare_parameter("audit_topic", "/audit/events")
        self.declare_parameter("friendly_ouis", ["D8:3A:DD", "B8:27:EB"])

        in_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        out_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(String, self.get_parameter("rf_topic").value, self._on_rf, in_qos)
        self.publisher = self.create_publisher(String, self.get_parameter("output_topic").value, out_qos)
        self.audit_pub = self.create_publisher(String, self.get_parameter("audit_topic").value, out_qos)

        self.friendly_ouis = {x.upper() for x in self.get_parameter("friendly_ouis").value}
        self.last_ledger_hash = "genesis"
        self.get_logger().info("cyber_node initialized")

    def _publish_ledger_event(self, assessment: IdentityAssessment) -> None:
        entry = {
            "event": "identity_assessment",
            "emitter_id": assessment.emitter_id,
            "disposition": assessment.disposition,
            "confidence": assessment.confidence,
            "prev_hash": self.last_ledger_hash,
        }
        digest = hashlib.sha256(json.dumps(entry, sort_keys=True).encode("utf-8")).hexdigest()
        entry["hash"] = digest
        self.last_ledger_hash = digest

        msg = String()
        msg.data = json.dumps(entry)
        self.audit_pub.publish(msg)

    def _derive_identity(self, rf_payload: dict) -> IdentityAssessment:
        fp = rf_payload.get("fingerprints", [{}])[0]
        emitter_id = str(fp.get("emitter_id", "unknown-emitter"))
        mac_oui = "D8:3A:DD" if emitter_id.endswith("0") else "AA:BB:CC"

        if mac_oui in self.friendly_ouis:
            disposition = "friendly"
            conf = 0.85
            vendor = "known_vendor"
        else:
            disposition = "unknown_or_hostile"
            conf = 0.78
            vendor = "untrusted_vendor"

        return IdentityAssessment(
            emitter_id=emitter_id,
            mac_oui=mac_oui,
            vendor_guess=vendor,
            rf_fingerprint_family=str(fp.get("modulation_guess", "unknown")),
            disposition=disposition,
            confidence=conf,
        )

    def _on_rf(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rf payload in cyber_node")
            return

        assessment = self._derive_identity(payload)
        out_msg = String()
        out_msg.data = json.dumps({"assessments": [asdict(assessment)]})
        self.publisher.publish(out_msg)
        self._publish_ledger_event(assessment)


def main() -> None:
    rclpy.init()
    node = CyberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
