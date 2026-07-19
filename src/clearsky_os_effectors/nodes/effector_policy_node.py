#!/usr/bin/env python3
"""ClearSky OS non-kinetic effector selection policy.

Simulation-safe, defensive C-UAS only. Selects among layered non-kinetic
effector modes from the fused track stream and publishes a human-gated plan
on /effector/selected_plan. All outputs are monitor-only unless the safety
gate is open AND an authorized engagement gate is granted by the operator.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String

_PKG = Path(__file__).resolve().parents[1]
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from clearsky_os_effectors.envelopes import success_probability, track_range_m  # noqa: E402


EFFECTOR_SOURCE = "clearsky_os_effectors"


EFFECTOR_CATALOG: Tuple[Dict[str, Any], ...] = (
    {
        "mode": "monitor",
        "family": "passive",
        "min_score": 0.0,
        "rationale": "Insufficient confidence for any effector; passive ISR only.",
        "kinetic": False,
        "human_gated": False,
    },
    {
        "mode": "multi_sensor_deception",
        "family": "deception",
        "min_score": 0.55,
        "rationale": "Inject benign decoy track to cross-validate adversary sensors and degrade their targeting.",
        "kinetic": False,
        "human_gated": True,
    },
    {
        "mode": "cognitive_jamming",
        "family": "rf_denial",
        "min_score": 0.65,
        "rationale": "Adaptive narrowband jamming on observed control-link emitter; minimal collateral RF footprint.",
        "kinetic": False,
        "human_gated": True,
    },
    {
        "mode": "gnss_link_spoofing",
        "family": "nav_denial",
        "min_score": 0.72,
        "rationale": "Localized GNSS/link spoofing to redirect target to safe geofence; coordinated with PNT resilience layer.",
        "kinetic": False,
        "human_gated": True,
    },
    {
        "mode": "hpm_denial_stub",
        "family": "directed_energy_sim",
        "min_score": 0.80,
        "rationale": "High-power microwave denial pulse simulation against incoming swarm element; non-kinetic defeat.",
        "kinetic": False,
        "human_gated": True,
    },
    {
        "mode": "control_link_takeover",
        "family": "cyber_takeover",
        "min_score": 0.88,
        "rationale": "Authorized cyber takeover of recovered control link to land target safely; requires explicit dual authorization.",
        "kinetic": False,
        "human_gated": True,
        "requires_dual_auth": True,
    },
    {
        "mode": "kamikaze_ram",
        "family": "kinetic_ram",
        "min_score": 0.95,
        "rationale": "Last-resort simulated terminal ram: kinetic energy via direct impact only (no warhead); requires safety gate, dual human authorization, and simulate-only deploy registration.",
        "kinetic": True,
        "human_gated": True,
        "requires_dual_auth": True,
    },
)


def select_effector(
    score: float,
    safety_open: bool,
    dual_auth: bool,
    enabled_families: Tuple[str, ...] = (
        "passive",
        "deception",
        "rf_denial",
        "nav_denial",
        "directed_energy_sim",
        "cyber_takeover",
        "kinetic_ram",
    ),
) -> Dict[str, Any]:
    """Select the highest-tier effector entry whose score threshold is met.

    Returns a copy of the catalog entry plus runtime metadata. When the
    safety gate is closed, output is forced to monitor-only regardless of
    the underlying selection.
    """
    eligible: List[Dict[str, Any]] = [
        entry
        for entry in EFFECTOR_CATALOG
        if entry["family"] in enabled_families and score >= float(entry["min_score"])
    ]
    chosen = eligible[-1] if eligible else dict(EFFECTOR_CATALOG[0])
    chosen = dict(chosen)
    requires_dual = bool(chosen.get("requires_dual_auth", False))
    authorized = (
        safety_open
        and chosen["mode"] != "monitor"
        and (dual_auth or not requires_dual)
    )
    chosen["score"] = score
    chosen["safety_open"] = safety_open
    chosen["dual_authorization_present"] = dual_auth
    chosen["authorized"] = authorized
    chosen["monitor_only"] = not authorized
    return chosen


class EffectorPolicyNode(Node):
    def __init__(self) -> None:
        super().__init__("effector_policy_node")
        self.declare_parameter("publish_hz", 2.0)
        self.declare_parameter(
            "enabled_families",
            [
                "passive",
                "deception",
                "rf_denial",
                "nav_denial",
                "directed_energy_sim",
                "cyber_takeover",
                "kinetic_ram",
            ],
        )
        self.declare_parameter("allow_kinetic_ram", False)
        self.declare_parameter("require_dual_authorization", True)

        self.safety_open = False
        self.dual_auth = False
        self.latest_track: Dict[str, Any] = {}
        self._last_plan: Dict[str, Any] = {}

        reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=20,
        )

        self.create_subscription(String, "/fused_tracks", self._on_fused, reliable_qos)
        self.create_subscription(String, "/safety_gate_status", self._on_safety, reliable_qos)
        self.create_subscription(
            String, "/operator/launch_authorizations", self._on_dual_auth, reliable_qos
        )

        self.plan_pub = self.create_publisher(String, "/effector/selected_plan", reliable_qos)
        self.kamikaze_auth_pub = self.create_publisher(String, "/effector/kamikaze_authorized", reliable_qos)
        self.audit_pub = self.create_publisher(String, "/audit/events", reliable_qos)

        publish_hz = max(0.2, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / publish_hz, self._tick)
        self.get_logger().info(
            "effector_policy_node initialized (simulation-safe, monitor-only by default)"
        )

    def _on_safety(self, msg: String) -> None:
        try:
            self.safety_open = bool(json.loads(msg.data).get("allow", False))
        except json.JSONDecodeError:
            self.safety_open = False

    def _on_dual_auth(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            self.dual_auth = False
            return
        approvals = payload.get("authorizations") or []
        approved = any(bool(a.get("approved", False)) for a in approvals)
        self.dual_auth = approved or bool(payload.get("approved", False))

    def _on_fused(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        tracks = payload.get("tracks") or []
        if not tracks:
            return
        # Pick the highest-confidence track for this tick.
        best = max(tracks, key=lambda t: float(t.get("confidence", 0.0)))
        self.latest_track = best

    def _enabled_families(self) -> Tuple[str, ...]:
        param = self.get_parameter("enabled_families").value
        if isinstance(param, (list, tuple)):
            families = [str(x) for x in param]
        else:
            families = ["passive"]
        if not bool(self.get_parameter("allow_kinetic_ram").value):
            families = [f for f in families if f != "kinetic_ram"]
        return tuple(families)

    def _tick(self) -> None:
        if not self.latest_track:
            return
        score = float(self.latest_track.get("confidence", 0.0))
        track_id = str(self.latest_track.get("track_id", "unknown"))
        require_dual = bool(self.get_parameter("require_dual_authorization").value)
        dual = self.dual_auth if require_dual else True
        chosen = select_effector(
            score=score,
            safety_open=self.safety_open,
            dual_auth=dual,
            enabled_families=self._enabled_families(),
        )
        kinetic_loop = bool(chosen.get("kinetic", False))
        range_m = track_range_m(self.latest_track)
        envelope = success_probability(str(chosen["mode"]), range_m, readiness=1.0)

        now = self.get_clock().now().to_msg()
        plan = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": EFFECTOR_SOURCE,
            "plan_id": f"eff-{int(time.time()*1000) % 10_000_000:07d}",
            "track_id": track_id,
            "selected": chosen,
            "catalog_considered": [e["mode"] for e in EFFECTOR_CATALOG],
            "policy": {
                "doctrine": "layered_non_kinetic_first_then_authorized_takeover_then_kinetic_ram_last_resort",
                "kinetic_in_loop": kinetic_loop,
                "human_authorization_required": True,
            },
            "envelope": envelope,
            "xai": {
                "rationale": chosen["rationale"],
                "score_threshold": chosen["min_score"],
                "score_observed": score,
                "monitor_only": chosen["monitor_only"],
                "range_m": envelope["range_m"],
                "path_loss_db": envelope["path_loss_db"],
                "success_probability": envelope["success_probability"],
                "envelope_model": "friis_logistic_v1",
            },
        }
        self._last_plan = plan
        self.plan_pub.publish(String(data=json.dumps(plan)))
        k_auth = {
            "authorized": bool(
                chosen.get("mode") == "kamikaze_ram"
                and chosen.get("authorized")
                and not chosen.get("monitor_only")
            ),
            "track_id": track_id,
            "plan_id": plan["plan_id"],
            "reason": "kamikaze_gates_ok" if chosen.get("mode") == "kamikaze_ram" else "not_kamikaze_or_monitor",
        }
        self.kamikaze_auth_pub.publish(String(data=json.dumps(k_auth)))
        self.audit_pub.publish(
            String(
                data=json.dumps(
                    {
                        "event": "effector_plan_published",
                        "plan_id": plan["plan_id"],
                        "track_id": track_id,
                        "mode": chosen["mode"],
                        "monitor_only": chosen["monitor_only"],
                    }
                )
            )
        )


def main() -> None:
    rclpy.init()
    node = EffectorPolicyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
