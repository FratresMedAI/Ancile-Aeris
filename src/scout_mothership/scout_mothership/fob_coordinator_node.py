#!/usr/bin/env python3
"""Aggregated FOB / micro-deployment views for mothership swarm (simulation)."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

import rclpy
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


def _make_inventory(node: Node) -> Dict[str, int]:
    return {
        "sensor_pod": int(node.get_parameter("mix_sensor_pod").value),
        "acoustic_disruptor": int(node.get_parameter("mix_acoustic_disruptor").value),
        "kevlar_web": int(node.get_parameter("mix_kevlar_web").value),
        "cognitive_ew_pod": int(node.get_parameter("mix_cognitive_ew_pod").value),
        "kamikaze_ram_slots": int(node.get_parameter("mix_kamikaze_ram_slots").value),
    }


class FobCoordinatorNode(Node):
    def __init__(self) -> None:
        super().__init__("fob_coordinator_node")
        self.declare_parameter("fob_count", 3)
        self.declare_parameter("micro_capacity_per_fob", 12)
        self.declare_parameter("publish_hz", 1.0)
        self.declare_parameter("profile", "mothership_fob_standard")
        self.declare_parameter("mix_sensor_pod", 4)
        self.declare_parameter("mix_acoustic_disruptor", 2)
        self.declare_parameter("mix_kevlar_web", 2)
        self.declare_parameter("mix_cognitive_ew_pod", 3)
        self.declare_parameter("mix_kamikaze_ram_slots", 1)

        self._inventory = _make_inventory(self)
        self._last_effector_mode: Optional[str] = None
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.fob_pub = self.create_publisher(String, "/mesh/fob_status", qos)
        self.deploy_pub = self.create_publisher(String, "/payload/micro_deployment", qos)
        self.create_subscription(String, "/effector/selected_plan", self._on_effector_plan, qos)
        hz = max(0.2, float(self.get_parameter("publish_hz").value))
        self.create_timer(1.0 / hz, self._tick)
        self.get_logger().info("fob_coordinator_node publishing /mesh/fob_status and /payload/micro_deployment")

    def _on_effector_plan(self, msg: String) -> None:
        try:
            payload = json.loads(msg.data)
        except json.JSONDecodeError:
            return
        selected = payload.get("selected") or {}
        mode = selected.get("mode")
        self._last_effector_mode = str(mode) if mode is not None else None

    def _effector_alignment(self) -> Dict[str, Any]:
        """Advisory only: correlate FOB micro inventory narrative with ship-level effector doctrine (simulation)."""
        mode = self._last_effector_mode
        if mode is None:
            return {
                "hint": "pending_effector_plan",
                "preferred_micro_roles": [],
                "notes": "Awaiting /effector/selected_plan for advisory alignment.",
            }
        if mode == "kamikaze_ram":
            return {
                "hint": "kinetic_ram_last_resort_sim_only",
                "preferred_micro_roles": ["kamikaze_ram_slots"],
                "notes": "Narrative alignment only; kinetic path requires dual human authorization and policy gates.",
            }
        return {
            "hint": "non_kinetic_micro_emphasis",
            "preferred_micro_roles": [
                "sensor_pod",
                "cognitive_ew_pod",
                "acoustic_disruptor",
                "kevlar_web",
            ],
            "notes": "Prefer ISR extension, EW, acoustic, and entanglement sim paths before any kinetic allocation story.",
        }

    def _fob_fleet(self) -> List[Dict[str, Any]]:
        n = max(2, min(4, int(self.get_parameter("fob_count").value)))
        cap = int(self.get_parameter("micro_capacity_per_fob").value)
        inv = self._inventory
        total_mix = sum(inv.values())
        if total_mix > cap:
            self.get_logger().warning(
                f"micro payload mix sums to {total_mix} > capacity {cap}; clamping display only"
            )
        fleet: List[Dict[str, Any]] = []
        for i in range(n):
            mid = f"mhs-{i+1:03d}"
            fleet.append(
                {
                    "mothership_id": mid,
                    "fob_index": i,
                    "geo_cell_id_sim": f"fob_cell_{i}",
                    "role": "mobile_forward_operating_base",
                    "coverage_mode": "persistent_FOB",
                    "micro_capacity": cap,
                    "micro_by_type": dict(inv),
                    "micro_total": total_mix,
                    "mesh_neighbors_expected": n - 1,
                }
            )
        return fleet

    def _tick(self) -> None:
        now = self.get_clock().now().to_msg()
        fleet = self._fob_fleet()
        fob_payload = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "mesh"},
            "producer": "fob_coordinator",
            "profile": str(self.get_parameter("profile").value),
            "fleet": fleet,
            "stamp": time.time(),
        }
        self.fob_pub.publish(String(data=json.dumps(fob_payload)))

        n = len(fleet)
        inv = self._inventory
        total_micro = n * sum(inv.values())
        dep = {
            "header": {"stamp": {"sec": now.sec, "nanosec": now.nanosec}, "frame_id": "map"},
            "producer": "fob_coordinator",
            "deployments": [
                {
                    "mothership_id": f["mothership_id"],
                    "payload_mix": dict(inv),
                    "ready_sim": True,
                    "hot_swap": True,
                }
                for f in fleet
            ],
            "fleet_total_micro_drones_sim": total_micro,
            "effector_alignment": self._effector_alignment(),
            "last_effector_mode_observed": self._last_effector_mode,
            "notes": "Simulation inventory; not flight hardware.",
            "stamp": time.time(),
        }
        self.deploy_pub.publish(String(data=json.dumps(dep)))


def main() -> None:
    rclpy.init()
    node = FobCoordinatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
