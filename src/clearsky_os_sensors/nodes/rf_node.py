#!/usr/bin/env python3
"""RF cueing node: spectral-peak heuristic or ONNX CNN when weights exist."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_sensors.rf_classifier import (  # noqa: E402
    classify_rf,
    result_as_dict,
    synthetic_iq,
)


@dataclass
class RfFingerprint:
    emitter_id: str
    confidence: float
    center_freq_hz: float
    bandwidth_hz: float
    modulation_guess: str
    source: str = "rf"
    backend: str = "heuristic_spectral_peak"
    class_label: str = "uas_control_link_candidate"


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class RfNode(Node):
    def __init__(self) -> None:
        super().__init__("rf_node")

        self.declare_parameter("model_name", "drone_rf_cnn")
        self.declare_parameter("publish_topic", "/sensor/rf/detections")
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("sim_mode", True)
        self.declare_parameter("onnx_path", "models/rf/drone_rf_cnn.onnx")
        self.declare_parameter("sample_rate_hz", 20.0e6)
        self.declare_parameter("rf_center_hz", 2.437e9)

        sim_default = bool(self.get_parameter("sim_mode").value)
        self.sim_mode = _env_flag("CLEARSKY_SIM_MODE", sim_default)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        publish_topic = self.get_parameter("publish_topic").get_parameter_value().string_value
        self.publisher = self.create_publisher(String, publish_topic, qos)

        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.05, 1.0 / publish_hz), self._tick)
        self.tick_count = 0
        self.onnx_path = Path(str(self.get_parameter("onnx_path").value))

        if not self.sim_mode and self.onnx_path.is_file():
            self.get_logger().info(f"rf_node using ONNX weights: {self.onnx_path}")
        else:
            self.get_logger().info(
                "rf_node using labeled spectral-peak heuristic "
                f"(sim_mode={self.sim_mode}; ONNX optional at models/rf/)"
            )

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()
        sr = float(self.get_parameter("sample_rate_hz").value)
        rf_c = float(self.get_parameter("rf_center_hz").value)
        iq = synthetic_iq(tick=self.tick_count, present=True, sample_rate_hz=sr)
        result = classify_rf(
            iq,
            sample_rate_hz=sr,
            rf_center_hz=rf_c,
            onnx_path=None if self.sim_mode else self.onnx_path,
            tick=self.tick_count,
            force_heuristic=self.sim_mode or not self.onnx_path.is_file(),
        )
        meta = result_as_dict(result)
        fingerprint = RfFingerprint(
            emitter_id=f"rf-{self.tick_count:05d}",
            confidence=float(meta["confidence"]),
            center_freq_hz=float(meta["center_freq_hz"]),
            bandwidth_hz=float(meta["bandwidth_hz"]),
            modulation_guess=str(meta["modulation_guess"]),
            backend=str(meta["backend"]),
            class_label=str(meta["class_label"]),
        )

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "rf_sensor_frame",
            },
            "model": self.get_parameter("model_name").value,
            "backend": fingerprint.backend,
            "fingerprints": [asdict(fingerprint)],
            "features": meta.get("features", {}),
            "latency_ms": 14.0 if fingerprint.backend.startswith("heuristic") else 28.0,
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = RfNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
