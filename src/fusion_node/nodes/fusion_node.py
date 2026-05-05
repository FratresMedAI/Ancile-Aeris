#!/usr/bin/env python3
import json
import os
from collections import deque
from dataclasses import asdict, dataclass

import rclpy
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
        self.declare_parameter("acoustic_topic", "/sensor/acoustic/detections")
        self.declare_parameter("rf_topic", "/sensor/rf/detections")
        self.declare_parameter("lidar_topic", "/sensor/lidar/points")
        self.declare_parameter("sigint_topic", "/sensor/sigint/elint")
        self.declare_parameter("video_analytics_topic", "/sensor/visual/analytics")
        self.declare_parameter("hyperspectral_topic", "/sensor/hyperspectral/observations")
        self.declare_parameter("neuromorphic_topic", "/neuromorphic_events")
        self.declare_parameter("sensor_health_topic", "/sensor_health")
        self.declare_parameter("adversarial_alert_topic", "/adversarial_alert")
        self.declare_parameter("fused_topic", "/fused_tracks")
        self.declare_parameter("publish_hz", 20.0)
        self.declare_parameter("min_confidence", 0.5)
        self.declare_parameter("pid_gate", 0.999)
        self.declare_parameter("fusion_model", "perceiver_io_stub")
        self.declare_parameter("onnx_model_path", "")

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

        self.visual_obs = deque(maxlen=20)
        self.acoustic_obs = deque(maxlen=20)
        self.rf_obs = deque(maxlen=20)
        self.lidar_obs = deque(maxlen=20)
        self.sigint_obs = deque(maxlen=20)
        self.video_analytics_obs = deque(maxlen=20)
        self.hyperspectral_obs = deque(maxlen=20)
        self.neuromorphic_obs = deque(maxlen=50)
        self.sensor_health_obs = deque(maxlen=20)
        self.adversarial_alert_obs = deque(maxlen=20)
        self.state = {"x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0}
        self.track_idx = 0
        self.onnx_backend = self._load_tensorrt_onnx_backend_stub()

        self.create_subscription(String, self.get_parameter("visual_topic").value, self._on_visual, sensor_qos)
        self.create_subscription(String, self.get_parameter("acoustic_topic").value, self._on_acoustic, sensor_qos)
        self.create_subscription(String, self.get_parameter("rf_topic").value, self._on_rf, sensor_qos)
        self.create_subscription(String, self.get_parameter("lidar_topic").value, self._on_lidar, sensor_qos)
        self.create_subscription(String, self.get_parameter("sigint_topic").value, self._on_sigint, sensor_qos)
        self.create_subscription(
            String, self.get_parameter("video_analytics_topic").value, self._on_video_analytics, sensor_qos
        )
        self.create_subscription(String, self.get_parameter("hyperspectral_topic").value, self._on_hyperspectral, sensor_qos)
        self.create_subscription(String, self.get_parameter("neuromorphic_topic").value, self._on_neuromorphic, sensor_qos)
        self.create_subscription(String, self.get_parameter("sensor_health_topic").value, self._on_sensor_health, c2_qos)
        self.create_subscription(
            String, self.get_parameter("adversarial_alert_topic").value, self._on_adversarial_alert, c2_qos
        )

        self.fused_pub = self.create_publisher(String, self.get_parameter("fused_topic").value, c2_qos)
        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.02, 1.0 / publish_hz), self._tick)

        self.get_logger().info("fusion_node initialized")

    def _load_tensorrt_onnx_backend_stub(self) -> str:
        model_path = str(self.get_parameter("onnx_model_path").value or "").strip()
        model_path = model_path or os.getenv("ANCILE_ONNX_MODEL_PATH", "").strip()
        if not model_path:
            return "stub_no_model"
        if not os.path.exists(model_path):
            self.get_logger().warning(f"ONNX model path not found: {model_path}")
            return "stub_missing_model"
        try:
            import tensorrt  # type: ignore  # noqa: F401
            self.get_logger().info(f"TensorRT ONNX stub ready for model: {model_path}")
            return "stub_tensorrt_available"
        except Exception as exc:
            self.get_logger().warning(f"TensorRT unavailable, staying in stub mode: {exc}")
            return "stub_tensorrt_unavailable"

    def _on_visual(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.visual_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid visual payload")

    def _on_acoustic(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.acoustic_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid acoustic payload")

    def _on_rf(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.rf_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid rf payload")

    def _on_lidar(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.lidar_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid lidar payload")

    def _on_sigint(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.sigint_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid sigint payload")

    def _on_video_analytics(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.video_analytics_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid video analytics payload")

    def _on_neuromorphic(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.neuromorphic_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid neuromorphic payload")

    def _on_hyperspectral(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.hyperspectral_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid hyperspectral payload")

    def _on_sensor_health(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.sensor_health_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid sensor health payload")

    def _on_adversarial_alert(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            self.adversarial_alert_obs.append(payload)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid adversarial alert payload")

    def _confidence_vote(self) -> float:
        visual_conf = 0.0
        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            visual_conf = float(self.visual_obs[-1]["tracks"][0].get("confidence", 0.0))

        acoustic_conf = 0.0
        if self.acoustic_obs and self.acoustic_obs[-1].get("detections"):
            acoustic_conf = float(self.acoustic_obs[-1]["detections"][0].get("confidence", 0.0))

        rf_conf = 0.0
        if self.rf_obs and self.rf_obs[-1].get("fingerprints"):
            rf_conf = float(self.rf_obs[-1]["fingerprints"][0].get("confidence", 0.0))

        lidar_conf = 0.0
        if self.lidar_obs and self.lidar_obs[-1].get("detections"):
            lidar_conf = float(self.lidar_obs[-1]["detections"][0].get("confidence", 0.0))

        sigint_conf = 0.0
        if self.sigint_obs:
            sigint_conf = float(self.sigint_obs[-1].get("confidence", 0.0))
        video_conf = 0.0
        if self.video_analytics_obs:
            latest_video = self.video_analytics_obs[-1]
            if latest_video.get("video_analytics"):
                video_conf = float(latest_video["video_analytics"][0].get("confidence", 0.0))
            else:
                video_conf = float(latest_video.get("confidence", 0.65))

        neuromorphic_conf = 0.0
        if self.neuromorphic_obs:
            neuromorphic_conf = float(self.neuromorphic_obs[-1].get("confidence", 0.0))
        hyperspectral_conf = 0.0
        if self.hyperspectral_obs:
            hyperspectral_conf = float(self.hyperspectral_obs[-1].get("confidence", 0.0))

        health_penalty = self._sensor_health_penalty()

        return (
            max(
                0.0,
                0.26 * visual_conf
                + 0.16 * acoustic_conf
                + 0.16 * rf_conf
                + 0.10 * lidar_conf
                + 0.08 * sigint_conf
                + 0.14 * video_conf
                + 0.08 * neuromorphic_conf
                + 0.08 * hyperspectral_conf
                - health_penalty,
            )
        )

    def _modalities_present(self) -> list[str]:
        present: list[str] = []
        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            present.append("visual")
        if self.acoustic_obs and self.acoustic_obs[-1].get("detections"):
            present.append("acoustic")
        if self.rf_obs and self.rf_obs[-1].get("fingerprints"):
            present.append("rf")
        if self.lidar_obs and self.lidar_obs[-1].get("detections"):
            present.append("lidar")
        if self.sigint_obs:
            present.append("sigint")
        if self.video_analytics_obs:
            present.append("video_analytics")
        if self.neuromorphic_obs:
            present.append("neuromorphic")
        if self.hyperspectral_obs:
            present.append("hyperspectral")
        return present

    def _sensor_health_penalty(self) -> float:
        penalty = 0.0
        if self.sensor_health_obs:
            latest = self.sensor_health_obs[-1]
            health_score = float(latest.get("health_score", 1.0))
            penalty += max(0.0, 1.0 - health_score) * 0.12
            if bool(latest.get("spoof_suspected", False)):
                penalty += 0.18
        if self.adversarial_alert_obs:
            latest_alert = self.adversarial_alert_obs[-1]
            if str(latest_alert.get("severity", "")).lower() in {"medium", "high", "critical"}:
                penalty += 0.20
        return min(0.5, penalty)

    def _ekf_predict_update(self) -> None:
        self.state["x"] += self.state["vx"] * 0.05
        self.state["y"] += self.state["vy"] * 0.05

        if self.visual_obs and self.visual_obs[-1].get("tracks"):
            trk = self.visual_obs[-1]["tracks"][0]
            mx = float(trk.get("x", 0.0))
            my = float(trk.get("y", 0.0))
            alpha = 0.35
            prev_x = self.state["x"]
            prev_y = self.state["y"]
            self.state["x"] = (1.0 - alpha) * self.state["x"] + alpha * mx
            self.state["y"] = (1.0 - alpha) * self.state["y"] + alpha * my
            self.state["vx"] = (self.state["x"] - prev_x) / 0.05
            self.state["vy"] = (self.state["y"] - prev_y) / 0.05

    def _uncertainty(self, conf: float, modalities: list[str]) -> dict:
        modality_score = min(1.0, len(set(modalities)) / 8.0)
        epistemic = round(max(0.0, 1.0 - modality_score), 4)
        aleatoric = round(min(1.0, max(0.0, 1.0 - conf) + self._sensor_health_penalty()), 4)
        total = round(min(1.0, 0.55 * epistemic + 0.45 * aleatoric), 4)
        return {
            "epistemic": epistemic,
            "aleatoric": aleatoric,
            "total": total,
            "confidence_interval": [round(max(0.0, conf - total), 4), round(min(1.0, conf + total), 4)],
        }

    def _tick(self) -> None:
        self._ekf_predict_update()
        conf = self._confidence_vote()
        if conf < float(self.get_parameter("min_confidence").value):
            return

        modalities = self._modalities_present()
        required = {"visual", "acoustic", "rf"}
        pid_gate = float(self.get_parameter("pid_gate").value)
        pid_passed = required.issubset(set(modalities)) and conf >= pid_gate

        self.track_idx += 1
        fused = FusedTrack(
            track_id=f"fused-{self.track_idx:05d}",
            x=self.state["x"],
            y=self.state["y"],
            vx=self.state["vx"],
            vy=self.state["vy"],
            confidence=conf,
            class_label="hostile_candidate" if pid_passed else "unconfirmed",
        )

        now = self.get_clock().now().to_msg()
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "tracks": [asdict(fused)],
            "fusion": {
                "method": "multimodal_cross_attention_transformer_stub",
                "model": str(self.get_parameter("fusion_model").value),
                "onnx_backend": self.onnx_backend,
                "sources": [
                    "visual",
                    "acoustic",
                    "rf",
                    "lidar",
                    "sigint",
                    "video_analytics",
                    "neuromorphic",
                    "hyperspectral",
                ],
                "adversarial_resilience": {
                    "sensor_health_penalty": self._sensor_health_penalty(),
                    "latest_alert": self.adversarial_alert_obs[-1] if self.adversarial_alert_obs else None,
                },
            },
            "pid": {
                "gate": pid_gate,
                "confidence": conf,
                "required_modalities": sorted(required),
                "present_modalities": modalities,
                "passed": pid_passed,
            },
            "uncertainty": self._uncertainty(conf, modalities),
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.fused_pub.publish(msg)


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
