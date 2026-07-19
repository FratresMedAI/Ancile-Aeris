#!/usr/bin/env python3
"""ClearSky OS high-altitude ISR scout mothership with mesh coordination (C-UAS defensive-only)."""

from __future__ import annotations

import json
import time
from typing import Any, Dict

import rclpy
from clearsky_os_integration import ClearSkyAuditBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

SCOUT_SOURCE = "clearsky_os_scout_mothership"


def loiter_profile() -> dict:
    return {
        "altitude_m": 4500.0,
        "endurance_hr": 24.0,
        "sensors": ["eo_ir", "rf", "acoustic"],
    }


def _arson_carrier_counterterror_signal(sim_phase: int) -> Dict[str, Any]:
    """Simulation-only counter-terror arson / incendiary precursor pattern."""
    hot = (sim_phase % 7) == 0
    return {
        "arson_carrier_precursor_sim": {
            "present": hot,
            "score": 0.88 if hot else 0.12,
            "basis_ct": ["thermal_hotspot_correlation", "loiter_above_refined_fuels_corr", "crowd_overlap_risk_stub"],
            "disposition": "indicative_only_simulation",
            "pid_gate_required": 0.999,
        }
    }


class ScoutMothershipNode(Node):
    def __init__(self) -> None:
        super().__init__("clearsky_os_scout_mothership_node")
        self.declare_parameter("publish_hz", 1.0)
        self.declare_parameter("confidence", 0.92)
        self.declare_parameter("mothership_id", "mhs-001")
        self.declare_parameter("mesh_enabled", True)
        self.declare_parameter("mesh_peer_count", 2)
        # Backward compatible aliases used in older configs.
        self.declare_parameter("enable_mesh_publish", True)
        self.declare_parameter("mesh_neighbor_count_hint", 2)

        self.safety_open = False
        self.launch_authorized = False
        self.track_idx = 0
        self._peer_seen: Dict[str, float] = {}
        self.audit_bridge = ClearSkyAuditBridge(self, SCOUT_SOURCE)

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )
        self.create_subscription(String, "/fused_tracks", self._on_fused, reliable_qos)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, reliable_qos)
        self.create_subscription(String, "/operator/launch_authorizations", self._on_launch_auth, reliable_qos)
        self.create_subscription(String, "/mesh/mothership_peers/heartbeat", self._on_mesh_peer_hb, reliable_qos)

        self.fused_pub = self.create_publisher(String, "/fused_tracks", reliable_qos)
        self.scout_pub = self.create_publisher(String, "/scout_eyes", reliable_qos)
        self.handoff_pub = self.create_publisher(String, "/interceptor_handoff", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)
        self.mesh_swarm_pub = self.create_publisher(String, "/mesh/mothership_swarm_status", reliable_qos)

        publish_hz = max(0.2, float(self.get_parameter("publish_hz").value))
        self.timer = self.create_timer(1.0 / publish_hz, self._publish_scout_overlay)
        self.get_logger().info("clearsky_os_scout_mothership_node initialized (mesh networking enabled when configured)")

    def _mothership_id(self) -> str:
        return str(self.get_parameter("mothership_id").value)

    def _mesh_enabled(self) -> bool:
        return bool(self.get_parameter("mesh_enabled").value) or bool(self.get_parameter("enable_mesh_publish").value)

    def _mesh_peer_count(self) -> int:
        peers = int(self.get_parameter("mesh_peer_count").value)
        if peers <= 0:
            peers = int(self.get_parameter("mesh_neighbor_count_hint").value)
        return max(1, peers)

    def _on_safety(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_launch_auth(self, msg: String) -> None:
        try:
            self.launch_authorized = bool(json.loads(msg.data).get("approved", False))
        except json.JSONDecodeError:
            self.launch_authorized = False

    def _on_mesh_peer_hb(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        peer = str(payload.get("mothership_id", ""))
        if peer and peer != self._mothership_id():
            self._peer_seen[peer] = time.monotonic()

    def _prune_peers(self) -> None:
        now = time.monotonic()
        stale = [pid for pid, seen in self._peer_seen.items() if now - seen > 15.0]
        for pid in stale:
            del self._peer_seen[pid]

    def _publish_mesh_swarm_status(self, coverage_cell: str) -> None:
        if not self._mesh_enabled():
            return
        self._prune_peers()
        now = self.get_clock().now().to_msg()
        members = [{"mothership_id": self._mothership_id(), "role": "coordinator_sim", "coverage_cell": coverage_cell}]
        for pid in sorted(self._peer_seen.keys()):
            members.append({"mothership_id": pid, "role": "mesh_peer_sim", "coverage_cell": "adjacent_stub"})
        mesh_payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "mesh"},
            "producer": SCOUT_SOURCE,
            "coordinated_coverage": {
                "sectors_assigned": [coverage_cell, "perimeter_alpha", "perimeter_bravo"],
                "redundancy_factor": self._mesh_peer_count(),
            },
            "members": members,
            "mesh_quality": {"latency_budget_ms": 120, "link_health_sim": "nominal"},
        }
        self.mesh_swarm_pub.publish(String(data=json.dumps(mesh_payload)))
        self.audit_bridge.emit(
            "mesh_swarm_publish",
            mesh_payload,
            xai_text="Simulation mesh ISR status for coordinated mothership coverage (C-UAS defensive posture).",
        )

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        if payload.get("producer") == SCOUT_SOURCE:
            return
        tracks = payload.get("tracks", [])
        if not tracks:
            return
        first = tracks[0]
        scout_packet = self._scout_packet(
            track_id=str(first.get("track_id", "unknown")),
            x=float(first.get("x", 0.0)),
            y=float(first.get("y", 0.0)),
            confidence=float(first.get("confidence", 0.0)),
        )
        self.scout_pub.publish(String(data=json.dumps(scout_packet)))
        self._publish_handoff(scout_packet["track_id"])

    def _publish_scout_overlay(self) -> None:
        self.track_idx += 1
        profile = loiter_profile()
        cell = f"grid_{self.track_idx % 5}"
        self._publish_mesh_swarm_status(cell)
        x = 120.0 + (self.track_idx % 15) * 2.5
        y = 80.0 + (self.track_idx % 11) * 1.5
        confidence = float(self.get_parameter("confidence").value)
        now = self.get_clock().now().to_msg()
        ct_signals = _arson_carrier_counterterror_signal(self.track_idx)
        track = {
            "track_id": f"scout-{self.track_idx:05d}",
            "x": x,
            "y": y,
            "vx": 2.5,
            "vy": 1.5,
            "altitude_m": profile["altitude_m"],
            "sensor_type": "high_altitude_eo_ir_rf",
            "confidence": confidence,
            "class_label": "scout_observed_uas_candidate",
            "source": SCOUT_SOURCE,
            "counterterror_threat_signals": ct_signals,
        }
        payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": SCOUT_SOURCE,
            "tracks": [track],
            "mesh": {"mothership_id": self._mothership_id(), "coverage_cell": cell},
            "fusion": {
                "method": "high_altitude_isr_overlay_sim_mesh",
                "model": "clearsky_os_scout_mothership_stub",
                "sources": profile["sensors"],
            },
            "pid": {
                "gate": 0.999,
                "confidence": confidence,
                "required_modalities": ["eo_ir", "rf"],
                "present_modalities": ["eo_ir", "rf", "acoustic"],
                "passed": False,
            },
        }
        self.fused_pub.publish(String(data=json.dumps(payload)))
        self.scout_pub.publish(String(data=json.dumps(self._scout_packet(track["track_id"], x, y, confidence))))

    def _scout_packet(self, track_id: str, x: float, y: float, confidence: float) -> dict:
        profile = loiter_profile()
        return {
            "track_id": track_id,
            "source": SCOUT_SOURCE,
            "mothership_id": self._mothership_id(),
            "x": x,
            "y": y,
            "altitude_m": profile["altitude_m"],
            "sensor_type": "high_altitude_eo_ir_rf",
            "confidence": confidence,
            "notes": "simulation_safe_high_altitude_isr_mesh",
        }

    def _publish_handoff(self, track_id: str) -> None:
        authorized_release = self.safety_open and self.launch_authorized
        handoff = {
            "engagement_id": f"handoff-{int(time.time())}",
            "track_id": track_id,
            "release_authorized": authorized_release,
            "requires_terminal_authorization": True,
            "monitor_only": not authorized_release,
            "mesh_mothership_id": self._mothership_id(),
        }
        self.handoff_pub.publish(String(data=json.dumps(handoff)))
        self.audit_pub.publish(String(data=json.dumps({"event": "scout_handoff", "handoff": handoff})))
        self.audit_bridge.emit(
            "scout_handoff",
            handoff,
            xai_text="Mesh-capable mothership ISR handoff simulation; release remains strictly human gated.",
        )


def main() -> None:
    rclpy.init()
    node = ScoutMothershipNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

