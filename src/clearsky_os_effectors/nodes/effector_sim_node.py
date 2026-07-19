#!/usr/bin/env python3
"""ClearSky OS effector health/state simulation publisher.

Publishes low-rate readiness telemetry plus analytic envelopes for each
non-kinetic effector mode so demos can visualize layered availability
without any real actuation.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_effectors.envelopes import (  # noqa: E402
    envelopes_for_catalog,
    track_range_m,
)


EFFECTOR_HEALTH: Dict[str, Dict[str, float]] = {
    "hpm_denial_stub": {"readiness": 0.92, "duty_cycle": 0.18},
    "cognitive_jamming": {"readiness": 0.97, "duty_cycle": 0.42},
    "gnss_link_spoofing": {"readiness": 0.88, "duty_cycle": 0.10},
    "control_link_takeover": {"readiness": 0.74, "duty_cycle": 0.04},
    "multi_sensor_deception": {"readiness": 0.95, "duty_cycle": 0.31},
}


class EffectorSimNode(Node):
    def __init__(self) -> None:
        super().__init__("effector_sim_node")
        self.declare_parameter("publish_hz", 0.5)
        self.declare_parameter("default_range_m", 800.0)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.latest_track: Dict[str, Any] = {}
        self.create_subscription(String, "/fused_tracks", self._on_fused, qos)
        self.pub = self.create_publisher(String, "/effector/status", qos)
        publish_hz = max(0.1, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / publish_hz, self._tick)
        self.get_logger().info(
            "effector_sim_node initialized (readiness + analytic envelopes)"
        )

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks") or []
        if not tracks:
            return
        self.latest_track = max(tracks, key=lambda t: float(t.get("confidence", 0.0)))

    def _tick(self) -> None:
        now = self.get_clock().now().to_msg()
        if self.latest_track:
            range_m = track_range_m(self.latest_track)
        else:
            range_m = float(self.get_parameter("default_range_m").value)
        readiness = {mode: float(h["readiness"]) for mode, h in EFFECTOR_HEALTH.items()}
        envelopes = envelopes_for_catalog(range_m, readiness)
        modes: Dict[str, Dict[str, float]] = {}
        for mode, health in EFFECTOR_HEALTH.items():
            env = envelopes.get(mode, {})
            modes[mode] = {
                **health,
                "range_m": float(env.get("range_m", range_m)),
                "path_loss_db": float(env.get("path_loss_db", 0.0)),
                "snr_db": float(env.get("snr_db", 0.0)),
                "success_probability": float(env.get("success_probability", 0.0)),
                "max_range_m": float(env.get("max_range_m", 0.0)),
            }
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": "clearsky_os_effectors",
            "monitor_only": True,
            "range_m": range_m,
            "envelope_model": "friis_logistic_v1",
            "modes": modes,
        }
        self.pub.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = EffectorSimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
