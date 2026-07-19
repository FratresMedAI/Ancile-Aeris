#!/usr/bin/env python3
"""Visual perception node: real YOLO when enabled, honest synthetic otherwise."""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class VisualTrack:
    track_id: str
    cls: str
    confidence: float
    x: float
    y: float
    w: float
    h: float
    source: str = "visual"


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class VisualNode(Node):
    def __init__(self) -> None:
        super().__init__("visual_node")

        self.declare_parameter("model_name", "yolo11n")
        self.declare_parameter("weights_path", "models/visual/yolo11n.pt")
        self.declare_parameter("onnx_path", "models/visual/yolo11n.onnx")
        self.declare_parameter("engine_path", "models/visual/yolo11n.engine")
        self.declare_parameter("publish_topic", "/sensor/visual/tracks")
        self.declare_parameter("publish_fps", 15.0)
        self.declare_parameter("sim_mode", True)
        self.declare_parameter("source", "")  # camera index, video path, or empty
        self.declare_parameter("conf_threshold", 0.35)
        self.declare_parameter("imgsz", 640)

        # CLEARSKY_SIM_MODE overrides ROS param when set
        sim_default = bool(self.get_parameter("sim_mode").value)
        self.sim_mode = _env_flag("CLEARSKY_SIM_MODE", sim_default)

        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        publish_topic = self.get_parameter("publish_topic").get_parameter_value().string_value
        self.publisher = self.create_publisher(String, publish_topic, qos)

        fps = self.get_parameter("publish_fps").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.01, 1.0 / fps), self._tick)

        self.frame_idx = 0
        self.model = None
        self.cap = None
        self.backend = "synthetic_track"
        self._next_track_id = 1

        if not self.sim_mode:
            self._init_inference()
        else:
            self.get_logger().info(
                "visual_node in sim_mode: publishing labeled synthetic tracks (not model inference)"
            )

    def _resolve_weights(self) -> Path | None:
        candidates = [
            Path(str(self.get_parameter("weights_path").value)),
            Path(str(self.get_parameter("onnx_path").value)),
            Path(str(self.get_parameter("engine_path").value)),
        ]
        for path in candidates:
            if path.is_file():
                return path
        return None

    def _init_inference(self) -> None:
        weights = self._resolve_weights()
        if weights is None:
            self.get_logger().error(
                "sim_mode=false but no weights found under models/visual/; "
                "publishing empty tracks. Run scripts/download_visual_weights.py"
            )
            self.backend = "model_unavailable"
            return
        try:
            from ultralytics import YOLO  # type: ignore
        except ImportError:
            self.get_logger().error(
                "ultralytics not installed; pip install -r requirements-ml.txt "
                "or keep CLEARSKY_SIM_MODE=true"
            )
            self.backend = "model_unavailable"
            return

        try:
            self.model = YOLO(str(weights))
            self.backend = "ultralytics_yolo"
            self.get_logger().info(f"visual_node loaded weights: {weights}")
        except Exception as exc:  # noqa: BLE001
            self.get_logger().error(f"failed to load YOLO weights: {exc}")
            self.backend = "model_unavailable"
            self.model = None
            return

        source = str(self.get_parameter("source").value).strip()
        if not source:
            source = os.environ.get("CLEARSKY_VISUAL_SOURCE", "0")
        try:
            import cv2  # type: ignore

            # numeric camera index
            if source.isdigit():
                self.cap = cv2.VideoCapture(int(source))
            else:
                self.cap = cv2.VideoCapture(source)
            if not self.cap.isOpened():
                self.get_logger().error(f"cannot open visual source: {source}")
                self.cap = None
                self.backend = "source_unavailable"
        except ImportError:
            self.get_logger().error("opencv-python not installed; required for live inference")
            self.backend = "model_unavailable"
            self.model = None

    def _synthetic_tracks(self) -> list[VisualTrack]:
        # Labeled synthetic motion — moderate confidence, never masquerades as PID-perfect inference
        t = self.frame_idx
        x = 0.35 + 0.25 * ((t % 40) / 40.0)
        y = 0.40 + 0.05 * ((t % 20) / 20.0)
        return [
            VisualTrack(
                track_id=f"synth-{t:05d}",
                cls="drone",
                confidence=0.62,
                x=x,
                y=y,
                w=0.10,
                h=0.08,
            )
        ]

    def _infer_tracks(self) -> tuple[list[VisualTrack], float]:
        if self.model is None or self.cap is None:
            return [], 0.0
        import time as _time

        ok, frame = self.cap.read()
        if not ok or frame is None:
            # loop video files
            self.cap.set(0, 0)  # CAP_PROP_POS_FRAMES
            ok, frame = self.cap.read()
            if not ok or frame is None:
                return [], 0.0

        start = _time.perf_counter()
        conf_th = float(self.get_parameter("conf_threshold").value)
        imgsz = int(self.get_parameter("imgsz").value)
        results = self.model.predict(frame, conf=conf_th, imgsz=imgsz, verbose=False)
        latency_ms = (_time.perf_counter() - start) * 1000.0

        tracks: list[VisualTrack] = []
        if not results:
            return tracks, latency_ms
        result = results[0]
        h, w = frame.shape[:2]
        names = result.names if hasattr(result, "names") else {}
        boxes = getattr(result, "boxes", None)
        if boxes is None:
            return tracks, latency_ms
        for box in boxes:
            xyxy = box.xyxy[0].tolist()
            cls_id = int(box.cls[0]) if box.cls is not None else 0
            conf = float(box.conf[0]) if box.conf is not None else 0.0
            x1, y1, x2, y2 = xyxy
            bw = max(1e-6, x2 - x1)
            bh = max(1e-6, y2 - y1)
            cx = ((x1 + x2) / 2.0) / max(w, 1)
            cy = ((y1 + y2) / 2.0) / max(h, 1)
            label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else str(cls_id)
            tid = self._next_track_id
            self._next_track_id += 1
            tracks.append(
                VisualTrack(
                    track_id=f"vis-{tid:05d}",
                    cls=str(label),
                    confidence=conf,
                    x=cx,
                    y=cy,
                    w=bw / max(w, 1),
                    h=bh / max(h, 1),
                )
            )
        return tracks, latency_ms

    def _tick(self) -> None:
        self.frame_idx += 1
        now = self.get_clock().now().to_msg()
        tsec = time.time()

        latency_ms = 0.0
        inference = False
        if self.sim_mode or self.backend in {"model_unavailable", "source_unavailable", "synthetic_track"}:
            if self.sim_mode:
                tracks = self._synthetic_tracks()
                self.backend = "synthetic_track"
                latency_ms = 1.0
            else:
                tracks = []
                latency_ms = 0.0
        else:
            tracks, latency_ms = self._infer_tracks()
            inference = True

        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "camera_optical_frame",
            },
            "model": {
                "name": self.get_parameter("model_name").value,
                "backend": self.backend,
                "inference": inference,
            },
            "latency_ms": latency_ms,
            "tracks": [asdict(t) for t in tracks],
            "runtime": {"unix_time": tsec, "sim_mode": self.sim_mode},
        }

        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = VisualNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if getattr(node, "cap", None) is not None:
            node.cap.release()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
