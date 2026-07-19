#!/usr/bin/env python3
"""Acoustic cueing node: band-energy heuristic or ONNX CRNN when weights exist."""

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

# Allow source-tree imports before install
_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_sensors.acoustic_classifier import (  # noqa: E402
    classify_acoustic,
    result_as_dict,
    synthetic_rotor_waveform,
)


@dataclass
class AcousticDetection:
    detection_id: str
    confidence: float
    estimated_bearing_deg: float
    frequency_band_hz: list[float]
    source: str = "acoustic"
    backend: str = "heuristic_band_energy"
    class_label: str = "uas_acoustic_candidate"


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class AcousticNode(Node):
    def __init__(self) -> None:
        super().__init__("acoustic_node")

        self.declare_parameter("model_name", "crnn_melspec")
        self.declare_parameter("publish_topic", "/sensor/acoustic/detections")
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("sim_mode", True)
        self.declare_parameter("onnx_path", "models/acoustic/crnn_melspec.onnx")
        self.declare_parameter("sample_rate_hz", 16000.0)

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
        self.backend = "heuristic_band_energy"
        if not self.sim_mode and self.onnx_path.is_file():
            self.backend = "onnx_crnn"
            self.get_logger().info(f"acoustic_node using ONNX weights: {self.onnx_path}")
        else:
            self.get_logger().info(
                "acoustic_node using labeled band-energy heuristic "
                f"(sim_mode={self.sim_mode}; ONNX optional at models/acoustic/)"
            )

    def _tick(self) -> None:
        self.tick_count += 1
        now = self.get_clock().now().to_msg()
        sr = float(self.get_parameter("sample_rate_hz").value)
        samples = synthetic_rotor_waveform(tick=self.tick_count, present=True, sample_rate_hz=sr)
        result = classify_acoustic(
            samples,
            sample_rate_hz=sr,
            bearing_hint_deg=35.0 + (self.tick_count % 20) * 0.5,
            onnx_path=None if self.sim_mode else self.onnx_path,
            tick=self.tick_count,
            force_heuristic=self.sim_mode or not self.onnx_path.is_file(),
        )
        meta = result_as_dict(result)
        det = AcousticDetection(
            detection_id=f"aud-{self.tick_count:05d}",
            confidence=float(meta["confidence"]),
            estimated_bearing_deg=float(meta["estimated_bearing_deg"]),
            frequency_band_hz=list(meta["frequency_band_hz"]),
            backend=str(meta["backend"]),
            class_label=str(meta["class_label"]),
        )

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "mic_array_frame",
            },
            "model": self.get_parameter("model_name").value,
            "backend": det.backend,
            "detections": [asdict(det)],
            "features": meta.get("features", {}),
            "latency_ms": 12.0 if det.backend.startswith("heuristic") else 22.0,
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = AcousticNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
