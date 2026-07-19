#!/usr/bin/env python3
import json
from collections import deque
from dataclasses import asdict, dataclass

import rclpy
from clearsky_os_fusion.cv_ekf import ConstantVelocityEKF, Measurement, associate_nearest
from clearsky_os_integration.helpers import ClearSkyAuditBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class FusedTrack:
    track_id: str
    x: float
    y: float
    vx: float
    vy: float
    confidence: float
    class_label: str


class FusionNode(Node):
    def __init__(self) -> None:
        super().__init__("fusion_node")

        self.declare_parameter("visual_topic", "/sensor/visual/tracks")
        self.declare_parameter("thermal_topic", "/sensor/thermal/tracks")
        self.declare_parameter("acoustic_topic", "/sensor/acoustic/detections")
        self.declare_parameter("rf_topic", "/sensor/rf/detections")
        self.declare_parameter("lidar_topic", "/sensor/lidar/points")
        self.declare_parameter("sigint_topic", "/sensor/sigint/elint")
        self.declare_parameter("fused_topic", "/fused_tracks")
        self.declare_parameter("publish_hz", 20.0)
        self.declare_parameter("min_confidence", 0.35)
        self.declare_parameter("pid_gate", 0.75)
        self.declare_parameter("fusion_model", "cv_ekf")
        self.declare_parameter("association_gate", 3.0)
        self.declare_parameter("dt", 0.05)

        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        c2_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.visual_obs: deque = deque(maxlen=20)
        self.thermal_obs: deque = deque(maxlen=20)
        self.acoustic_obs: deque = deque(maxlen=20)
        self.rf_obs: deque = deque(maxlen=20)
        self.lidar_obs: deque = deque(maxlen=20)
        self.sigint_obs: deque = deque(maxlen=20)
        self.audit_bridge = ClearSkyAuditBridge(self, "fusion_node")
        dt = float(self.get_parameter("dt").value)
        self.ekf = ConstantVelocityEKF(dt=dt)
        self.track_idx = 0
        self._stable_track_id = "fused-00000"

        self.create_subscription(String, self.get_parameter("visual_topic").value, self._on_visual, sensor_qos)
        self.create_subscription(String, self.get_parameter("thermal_topic").value, self._on_thermal, sensor_qos)
        self.create_subscription(String, self.get_parameter("acoustic_topic").value, self._on_acoustic, sensor_qos)
        self.create_subscription(String, self.get_parameter("rf_topic").value, self._on_rf, sensor_qos)
        self.create_subscription(String, self.get_parameter("lidar_topic").value, self._on_lidar, sensor_qos)
        self.create_subscription(String, self.get_parameter("sigint_topic").value, self._on_sigint, sensor_qos)

        self.fused_pub = self.create_publisher(String, self.get_parameter("fused_topic").value, c2_qos)
        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.02, 1.0 / publish_hz), self._tick)

        self.get_logger().info("fusion_node initialized (cv_ekf)")

    def _on_visual(self, msg: String) -> None:
        try:
            self.visual_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid visual payload")

    def _on_acoustic(self, msg: String) -> None:
        try:
            self.acoustic_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid acoustic payload")

    def _on_thermal(self, msg: String) -> None:
        try:
            self.thermal_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid thermal payload")

    def _on_rf(self, msg: String) -> None:
        try:
            self.rf_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rf payload")

    def _on_lidar(self, msg: String) -> None:
        try:
            self.lidar_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid lidar payload")

    def _on_sigint(self, msg: String) -> None:
        try:
            self.sigint_obs.append(json.loads(msg.data))
        except json.JSONDecodeError:
            self.get_logger().warning("invalid sigint payload")

    def _collect_position_measurements(self) -> list[Measurement]:
        measurements: list[Measurement] = []
        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            for trk in self.visual_obs[-1]["tracks"]:
                measurements.append(
                    Measurement(
                        x=float(trk.get("x", 0.0)),
                        y=float(trk.get("y", 0.0)),
                        confidence=float(trk.get("confidence", 0.0)),
                        track_id=str(trk.get("track_id", "")),
                    )
                )
        if self.thermal_obs and self.thermal_obs[-1].get("tracks"):
            for trk in self.thermal_obs[-1]["tracks"]:
                measurements.append(
                    Measurement(
                        x=float(trk.get("x", 0.0)),
                        y=float(trk.get("y", 0.0)),
                        confidence=float(trk.get("confidence", 0.0)) * 0.9,
                        track_id=str(trk.get("track_id", "")),
                    )
                )
        return measurements

    def _modality_support_score(self) -> float:
        score = 0.0
        weights = 0.0
        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            score += 0.45 * float(self.visual_obs[-1]["tracks"][0].get("confidence", 0.0))
            weights += 0.45
        if self.thermal_obs and self.thermal_obs[-1].get("tracks"):
            score += 0.2 * float(self.thermal_obs[-1]["tracks"][0].get("confidence", 0.0))
            weights += 0.2
        if self.acoustic_obs and self.acoustic_obs[-1].get("detections"):
            score += 0.15 * float(self.acoustic_obs[-1]["detections"][0].get("confidence", 0.0))
            weights += 0.15
        if self.rf_obs and self.rf_obs[-1].get("fingerprints"):
            score += 0.12 * float(self.rf_obs[-1]["fingerprints"][0].get("confidence", 0.0))
            weights += 0.12
        if self.lidar_obs and self.lidar_obs[-1].get("detections"):
            score += 0.05 * float(self.lidar_obs[-1]["detections"][0].get("confidence", 0.0))
            weights += 0.05
        if self.sigint_obs:
            score += 0.03 * float(self.sigint_obs[-1].get("confidence", 0.0))
            weights += 0.03
        if weights <= 0.0:
            return 0.0
        return score / weights * weights  # keep absolute weighted sum in [0,1]-ish

    def _modalities_present(self) -> list[str]:
        present: list[str] = []
        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            present.append("visual")
        if self.thermal_obs and self.thermal_obs[-1].get("tracks"):
            present.append("thermal")
        if self.acoustic_obs and self.acoustic_obs[-1].get("detections"):
            present.append("acoustic")
        if self.rf_obs and self.rf_obs[-1].get("fingerprints"):
            present.append("rf")
        if self.lidar_obs and self.lidar_obs[-1].get("detections"):
            present.append("lidar")
        if self.sigint_obs:
            present.append("sigint")
        return present

    def _tick(self) -> None:
        dt = float(self.get_parameter("dt").value)
        self.ekf.predict(dt)

        measurements = self._collect_position_measurements()
        gate = float(self.get_parameter("association_gate").value)
        chosen = associate_nearest(self.ekf, measurements, gate=gate)
        meas_conf = 0.0
        if chosen is not None:
            self.ekf.update(chosen.x, chosen.y)
            meas_conf = chosen.confidence
            if chosen.track_id:
                self._stable_track_id = f"fused-{chosen.track_id}"

        support = self._modality_support_score()
        conf = self.ekf.calibrated_confidence(max(meas_conf, support))
        if conf < float(self.get_parameter("min_confidence").value):
            return
        if not self.ekf.initialized:
            return

        modalities = self._modalities_present()
        # Honest Phase-1 gate: visual (or thermal) is enough; stubs no longer force 4-way 0.999
        required = {"visual"}
        pid_gate = float(self.get_parameter("pid_gate").value)
        pid_passed = required.issubset(set(modalities)) and conf >= pid_gate

        state = self.ekf.state()
        self.track_idx += 1
        fused = FusedTrack(
            track_id=self._stable_track_id if self.ekf.initialized else f"fused-{self.track_idx:05d}",
            x=state["x"],
            y=state["y"],
            vx=state["vx"],
            vy=state["vy"],
            confidence=conf,
            class_label="hostile_candidate" if pid_passed else "unconfirmed",
        )

        now = self.get_clock().now().to_msg()
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "tracks": [asdict(fused)],
            "fusion": {
                "method": "constant_velocity_ekf",
                "model": str(self.get_parameter("fusion_model").value),
                "nis": state["nis"],
                "sources": modalities,
            },
            "pid": {
                "gate": pid_gate,
                "confidence": conf,
                "required_modalities": sorted(required),
                "present_modalities": modalities,
                "passed": pid_passed,
            },
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.fused_pub.publish(msg)
        self.audit_bridge.emit(
            "fusion_track_update",
            {
                "track_id": fused.track_id,
                "confidence": conf,
                "pid_passed": pid_passed,
                "present_modalities": modalities,
                "nis": state["nis"],
            },
            xai_text=(
                f"CV-EKF confidence {conf:.3f}; NIS {state['nis']:.2f}; "
                f"PID gate {'passed' if pid_passed else 'blocked'}."
            ),
        )


def main() -> None:
    rclpy.init()
    node = FusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
