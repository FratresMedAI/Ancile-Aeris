#!/usr/bin/env python3
import json
from collections import deque
from dataclasses import asdict, dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


@dataclass
class PredictedPoint:
    t_sec: float
    x: float
    y: float


@dataclass
class PredictedTrajectory:
    track_id: str
    points: list[PredictedPoint]
    confidence: float
    predictor: str


class TrajectoryNode(Node):
    def __init__(self) -> None:
        super().__init__("trajectory_node")

        self.declare_parameter("fused_tracks_topic", "/fused_tracks")
        self.declare_parameter("output_topic", "/predicted_trajectories")
        self.declare_parameter("prediction_horizon_sec", 3.0)
        self.declare_parameter("prediction_dt_sec", 0.5)
        self.declare_parameter("publish_hz", 10.0)
        self.declare_parameter("predictor_name", "kalman_plus_transformer_stub")

        self.track_buffer = deque(maxlen=30)
        self.latest_prediction = None

        in_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        out_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(
            String,
            self.get_parameter("fused_tracks_topic").value,
            self._on_fused_track,
            in_qos,
        )
        self.publisher = self.create_publisher(String, self.get_parameter("output_topic").value, out_qos)

        publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        self.timer = self.create_timer(max(0.05, 1.0 / publish_hz), self._tick)

        self.get_logger().info("trajectory_node initialized")

    def _on_fused_track(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
            tracks = payload.get("tracks", [])
            if not tracks:
                return
            track = tracks[0]
            self.track_buffer.append(track)
            self.latest_prediction = self._predict(track)
        except json.JSONDecodeError:
            self.get_logger().warning("invalid fused track payload")

    def _predict(self, track: dict) -> PredictedTrajectory:
        x = float(track.get("x", 0.0))
        y = float(track.get("y", 0.0))
        vx = float(track.get("vx", 0.0))
        vy = float(track.get("vy", 0.0))

        horizon = float(self.get_parameter("prediction_horizon_sec").value)
        dt = float(self.get_parameter("prediction_dt_sec").value)
        n_steps = max(1, int(horizon / dt))

        points: list[PredictedPoint] = []
        for i in range(1, n_steps + 1):
            t = i * dt
            points.append(PredictedPoint(t_sec=t, x=x + vx * t, y=y + vy * t))

        return PredictedTrajectory(
            track_id=str(track.get("track_id", "fused-unknown")),
            points=points,
            confidence=min(0.99, max(0.5, float(track.get("confidence", 0.5)))),
            predictor=str(self.get_parameter("predictor_name").value),
        )

    def _tick(self) -> None:
        if self.latest_prediction is None:
            return

        now = self.get_clock().now().to_msg()
        payload = {
            "header": {
                "stamp": {"sec": now.sec, "nanosec": now.nanosec},
                "frame_id": "map",
            },
            "predictions": [
                {
                    "track_id": self.latest_prediction.track_id,
                    "points": [asdict(p) for p in self.latest_prediction.points],
                    "confidence": self.latest_prediction.confidence,
                    "predictor": self.latest_prediction.predictor,
                }
            ],
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = TrajectoryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
