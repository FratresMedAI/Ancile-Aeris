#!/usr/bin/env python3
"""Digital twin: analytic now-cast or Gazebo-compatible kinematic rollout."""

from __future__ import annotations

import json
import time

import rclpy
from digital_twin.physics import evaluate_proposal
from digital_twin.rollout import RolloutConfig, evaluate_rollout
from rclpy.node import Node
from std_msgs.msg import String


class DigitalTwinNode(Node):
    def __init__(self) -> None:
        super().__init__("digital_twin_node")
        self.declare_parameter("risk_veto_threshold", 0.65)
        self.declare_parameter("asset_radius_m", 25.0)
        self.declare_parameter("publish_hz", 5.0)
        # analytic | gazebo_rollout
        self.declare_parameter("backend", "gazebo_rollout")
        self.declare_parameter("rollout_horizon_s", 3.0)
        self.declare_parameter("rollout_dt", 0.2)

        self.safety_open = False
        self.latest_track: dict = {}
        self.latest_truth: dict = {}
        self.latest_eval = None

        self.create_subscription(String, "/proposed_actions", self._on_proposal, 20)
        self.create_subscription(String, "/safety_gate_status", self._on_safety_status, 20)
        self.create_subscription(String, "/fused_tracks", self._on_fused, 20)
        self.create_subscription(String, "/sim/ground_truth", self._on_truth, 20)

        self.result_pub = self.create_publisher(String, "/digital_twin_result", 20)
        self.veto_pub = self.create_publisher(String, "/digital_twin/veto", 20)

        hz = float(self.get_parameter("publish_hz").value)
        self.create_timer(max(0.2, 1.0 / hz), self._publish_veto)
        self.get_logger().info(
            f"digital_twin_node initialized (backend={self.get_parameter('backend').value})"
        )

    def _on_safety_status(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_truth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        truth = payload.get("truth") or {}
        if truth:
            self.latest_truth = truth

    def _evaluate(
        self,
        *,
        track_x: float,
        track_y: float,
        track_vx: float,
        track_vy: float,
        threat_score: float,
        mitigation_gain: float,
    ):
        backend = str(self.get_parameter("backend").value)
        radius = float(self.get_parameter("asset_radius_m").value)
        thresh = float(self.get_parameter("risk_veto_threshold").value)
        if backend == "gazebo_rollout":
            truth_x = float(self.latest_truth["x"]) if "x" in self.latest_truth else None
            truth_y = float(self.latest_truth["y"]) if "y" in self.latest_truth else None
            return evaluate_rollout(
                track_x=track_x,
                track_y=track_y,
                track_vx=track_vx,
                track_vy=track_vy,
                threat_score=threat_score,
                mitigation_gain=mitigation_gain,
                safety_open=self.safety_open,
                truth_x=truth_x,
                truth_y=truth_y,
                cfg=RolloutConfig(
                    horizon_s=float(self.get_parameter("rollout_horizon_s").value),
                    dt=float(self.get_parameter("rollout_dt").value),
                    asset_radius_m=radius,
                    risk_veto_threshold=thresh,
                ),
            )
        return evaluate_proposal(
            track_x=track_x,
            track_y=track_y,
            track_vx=track_vx,
            track_vy=track_vy,
            threat_score=threat_score,
            mitigation_gain=mitigation_gain,
            asset_radius_m=radius,
            risk_veto_threshold=thresh,
            safety_open=self.safety_open,
        )

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks") or []
        if not tracks:
            return
        self.latest_track = tracks[0]
        self.latest_eval = self._evaluate(
            track_x=float(self.latest_track.get("x", 0.0)),
            track_y=float(self.latest_track.get("y", 0.0)),
            track_vx=float(self.latest_track.get("vx", 0.0)),
            track_vy=float(self.latest_track.get("vy", 0.0)),
            threat_score=float(self.latest_track.get("confidence", 0.5)),
            mitigation_gain=0.55,
        )

    def _on_proposal(self, msg: String) -> None:
        start = time.perf_counter()
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return

        track = self.latest_track
        evaluation = self._evaluate(
            track_x=float(track.get("x", payload.get("x", 0.0))),
            track_y=float(track.get("y", payload.get("y", 0.0))),
            track_vx=float(track.get("vx", payload.get("vx", 0.0))),
            track_vy=float(track.get("vy", payload.get("vy", 0.0))),
            threat_score=float(payload.get("score", track.get("confidence", 0.5))),
            mitigation_gain=float(payload.get("mitigation_gain", 0.6)),
        )
        self.latest_eval = evaluation
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        out = {
            "proposal_id": payload.get("proposal_id", "unknown"),
            "effectiveness_probability": evaluation.effectiveness_probability,
            "collateral_risk_score": evaluation.collateral_risk_score,
            "latency_ms": elapsed_ms,
            "generative_what_if": evaluation.rationale,
            "monitor_only": evaluation.veto or (not self.safety_open),
            "closing_speed_mps": evaluation.closing_speed_mps,
            "miss_distance_m": evaluation.miss_distance_m,
            "model": str(self.get_parameter("backend").value),
            "truth_available": bool(self.latest_truth),
        }
        self.result_pub.publish(String(data=json.dumps(out)))
        self._publish_veto()

    def _publish_veto(self) -> None:
        if self.latest_eval is None:
            payload = {"veto": False, "risk": 0.0, "source": "digital_twin", "ready": False}
        else:
            payload = {
                "veto": bool(self.latest_eval.veto),
                "risk": float(self.latest_eval.risk),
                "source": "digital_twin",
                "ready": True,
                "rationale": self.latest_eval.rationale,
                "backend": str(self.get_parameter("backend").value),
            }
        self.veto_pub.publish(String(data=json.dumps(payload)))


def main() -> None:
    rclpy.init()
    node = DigitalTwinNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
