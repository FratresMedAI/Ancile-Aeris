#!/usr/bin/env python3
"""ClearSky OS high-altitude ISR scout mothership with mesh coordination (C-UAS defensive-only).

Phase 2: enrich fused tracks (coverage / mesh / altitude). Does **not** invent
PID-passing tracks on /fused_tracks.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, Optional

import rclpy
from clearsky_os_integration import ClearSkyAuditBridge
from clearsky_os_scout_mothership.scout_enrichment import (
    SCOUT_SOURCE,
    coverage_cell_for_xy,
    enrich_track,
    loiter_profile,
)
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

# Re-export for tests / external imports
__all__ = [
    "SCOUT_SOURCE",
    "ScoutMothershipNode",
    "coverage_cell_for_xy",
    "enrich_track",
    "loiter_profile",
    "main",
]


class ScoutMothershipNode(Node):
    def __init__(self) -> None:
        super().__init__("clearsky_os_scout_mothership_node")
        self.declare_parameter("publish_hz", 1.0)
        self.declare_parameter("mothership_id", "mhs-001")
        self.declare_parameter("mesh_enabled", True)
        self.declare_parameter("mesh_peer_count", 2)
        # Backward compatible aliases used in older configs.
        self.declare_parameter("enable_mesh_publish", True)
        self.declare_parameter("mesh_neighbor_count_hint", 2)
        # Deprecated: ignored (scout no longer invents confidence tracks)
        self.declare_parameter("confidence", 0.0)

        self.safety_open = False
        self.launch_authorized = False
        self._peer_seen: Dict[str, float] = {}
        self._latest_track: Optional[Dict[str, Any]] = None
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

        # Enrichment + coordination only — do not republish invented /fused_tracks
        self.scout_pub = self.create_publisher(String, "/scout_eyes", reliable_qos)
        self.enrich_pub = self.create_publisher(String, "/scout/enrichment", reliable_qos)
        self.handoff_pub = self.create_publisher(String, "/interceptor_handoff", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)
        self.mesh_swarm_pub = self.create_publisher(String, "/mesh/mothership_swarm_status", reliable_qos)

        publish_hz = max(0.2, float(self.get_parameter("publish_hz").value))
        self.timer = self.create_timer(1.0 / publish_hz, self._publish_mesh_heartbeat)
        self.get_logger().info(
            "clearsky_os_scout_mothership_node initialized "
            "(enrichment-only; does not invent /fused_tracks)"
        )

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
            "tied_to_fused_track": self._latest_track is not None,
        }
        self.mesh_swarm_pub.publish(String(data=json.dumps(mesh_payload)))
        self.audit_bridge.emit(
            "mesh_swarm_publish",
            mesh_payload,
            xai_text="Mesh ISR coverage status; kinematics remain owned by fusion.",
        )

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        # Ignore any legacy scout-produced fused frames if present on the bus
        if payload.get("producer") == SCOUT_SOURCE:
            return
        tracks = payload.get("tracks", [])
        if not tracks:
            return
        best = max(tracks, key=lambda t: float(t.get("confidence", 0.0)))
        self._latest_track = best
        scout_packet = enrich_track(best, self._mothership_id(), self._mesh_peer_count())
        now = self.get_clock().now().to_msg()
        enrichment = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": SCOUT_SOURCE,
            "role": "enrichment",
            "track": scout_packet,
            "upstream_producer": payload.get("producer"),
        }
        self.scout_pub.publish(String(data=json.dumps(scout_packet)))
        self.enrich_pub.publish(String(data=json.dumps(enrichment)))
        self._publish_handoff(scout_packet["track_id"])
        self._publish_mesh_swarm_status(str(scout_packet["coverage_cell"]))

    def _publish_mesh_heartbeat(self) -> None:
        """Periodic mesh heartbeat; coverage cell from last fused track if any."""
        if self._latest_track is not None:
            cell = coverage_cell_for_xy(
                float(self._latest_track.get("x", 0.0)),
                float(self._latest_track.get("y", 0.0)),
            )
        else:
            cell = "grid_idle"
        self._publish_mesh_swarm_status(cell)

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
            xai_text="Mesh-capable mothership ISR handoff; release remains strictly human gated.",
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
