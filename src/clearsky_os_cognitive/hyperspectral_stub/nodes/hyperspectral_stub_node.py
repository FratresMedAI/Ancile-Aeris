#!/usr/bin/env python3
import json

import rclpy
from clearsky_os_integration import ClearSkyAuditBridge
from rclpy.node import Node
from std_msgs.msg import String


def classify_material(signature_energy: float) -> str:
    if signature_energy > 0.8:
        return "metallic_body"
    if signature_energy > 0.45:
        return "composite_material"
    return "unknown"


class HyperspectralStubNode(Node):
    def __init__(self) -> None:
        super().__init__("hyperspectral_stub_node")
        self.safety_open = False
        self.audit_bridge = ClearSkyAuditBridge(self, "hyperspectral_stub")
        self.create_subscription(String, "/sensor/hyperspectral/raw", self._on_raw, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.pub = self.create_publisher(String, "/sensor/hyperspectral/observations", 20)

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_raw(self, msg: String) -> None:
        # TODO: integrate real hyperspectral cube ingestion and spectral unmixing.
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        energy = float(payload.get("signature_energy", 0.0))
        out = {
            "sensor_id": payload.get("sensor_id", "hyperspectral_stub"),
            "material_class": classify_material(energy),
            "confidence": min(1.0, max(0.0, energy)),
            "anomaly_score": max(0.0, 1.0 - energy),
            "monitor_only": not self.safety_open,
        }
        self.pub.publish(String(data=json.dumps(out)))
        self.audit_bridge.emit(
            "hyperspectral_observation",
            out,
            xai_text="Hyperspectral stub estimated material class from simulated spectral energy.",
        )


def main() -> None:
    rclpy.init()
    node = HyperspectralStubNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
