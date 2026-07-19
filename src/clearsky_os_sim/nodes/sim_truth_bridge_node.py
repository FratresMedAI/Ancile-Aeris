#!/usr/bin/env python3
"""Publish Gazebo-compatible ground truth + optional metric sensor projections.

Does not require Gazebo at runtime. When override_sensors is true, publishes
onto the live ClearSky sensor topics for end-to-end twin/fusion demos.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_sim.kinematics import (  # noqa: E402
    ground_truth_payload,
    project_sensors,
    truth_at,
)


class SimTruthBridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("sim_truth_bridge_node")
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("override_sensors", False)
        self.declare_parameter("x0", 180.0)
        self.declare_parameter("y0", 40.0)
        self.declare_parameter("vx", -12.0)
        self.declare_parameter("vy", 2.0)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        self.truth_pub = self.create_publisher(String, "/sim/ground_truth", qos)
        self.override = bool(self.get_parameter("override_sensors").value)
        if self.override:
            self.visual_pub = self.create_publisher(String, "/sensor/visual/tracks", sensor_qos)
            self.thermal_pub = self.create_publisher(String, "/sensor/thermal/tracks", sensor_qos)
            self.acoustic_pub = self.create_publisher(String, "/sensor/acoustic/detections", sensor_qos)
            self.rf_pub = self.create_publisher(String, "/sensor/rf/detections", sensor_qos)
            self.lidar_pub = self.create_publisher(String, "/sensor/lidar/points", sensor_qos)

        self.tick = 0
        self.t0 = None
        hz = max(1.0, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / hz, self._tick)
        self.get_logger().info(
            f"sim_truth_bridge_node ready (override_sensors={self.override}; "
            "Gazebo SDF optional at share/clearsky_os_sim/worlds/clearsky_cuas.sdf)"
        )

    def _tick(self) -> None:
        now = self.get_clock().now()
        if self.t0 is None:
            self.t0 = now
        t = (now - self.t0).nanoseconds * 1e-9
        self.tick += 1
        state = truth_at(
            t,
            x0=float(self.get_parameter("x0").value),
            y0=float(self.get_parameter("y0").value),
            vx=float(self.get_parameter("vx").value),
            vy=float(self.get_parameter("vy").value),
        )
        stamp = now.to_msg()
        truth = ground_truth_payload(state, self.tick)
        truth["header"] = {"stamp": {"sec": stamp.sec, "nanosec": stamp.nanosec}, "frame_id": "map"}
        self.truth_pub.publish(String(data=json.dumps(truth)))

        if not self.override:
            return
        proj = project_sensors(state, tick=self.tick)
        for key, pub_attr in (
            ("visual", "visual_pub"),
            ("thermal", "thermal_pub"),
            ("acoustic", "acoustic_pub"),
            ("rf", "rf_pub"),
            ("lidar", "lidar_pub"),
        ):
            payload = proj[key]
            payload["header"] = {
                "stamp": {"sec": stamp.sec, "nanosec": stamp.nanosec},
                "frame_id": "map",
            }
            getattr(self, pub_attr).publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = SimTruthBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
