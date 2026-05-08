import importlib.util
import os
import sys
import types


def _load_module():
    here = os.path.dirname(os.path.abspath(__file__))
    node_path = os.path.normpath(os.path.join(here, "..", "nodes", "effector_policy_node.py"))

    for name in ("rclpy", "rclpy.node", "rclpy.qos", "std_msgs", "std_msgs.msg"):
        sys.modules.setdefault(name, types.ModuleType(name))
    sys.modules["rclpy.node"].Node = type("Node", (), {})
    sys.modules["rclpy.qos"].HistoryPolicy = types.SimpleNamespace(KEEP_LAST=0)
    sys.modules["rclpy.qos"].ReliabilityPolicy = types.SimpleNamespace(RELIABLE=0)
    sys.modules["rclpy.qos"].QoSProfile = lambda **_: None
    sys.modules["std_msgs.msg"].String = type("String", (), {})

    spec = importlib.util.spec_from_file_location("effector_policy_node", node_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


_MODULE = _load_module()
select_effector = _MODULE.select_effector
EFFECTOR_CATALOG = _MODULE.EFFECTOR_CATALOG


def test_low_score_is_monitor() -> None:
    chosen = select_effector(score=0.1, safety_open=True, dual_auth=True)
    assert chosen["mode"] == "monitor"
    assert chosen["monitor_only"] is True


def test_safety_closed_forces_monitor_only() -> None:
    chosen = select_effector(score=0.95, safety_open=False, dual_auth=True)
    assert chosen["monitor_only"] is True
    assert chosen["authorized"] is False


def test_layered_escalation() -> None:
    low = select_effector(score=0.60, safety_open=True, dual_auth=True)
    mid = select_effector(score=0.74, safety_open=True, dual_auth=True)
    high = select_effector(score=0.90, safety_open=True, dual_auth=True)
    assert low["mode"] in {"multi_sensor_deception", "cognitive_jamming"}
    assert mid["mode"] in {"gnss_link_spoofing", "cognitive_jamming"}
    assert high["mode"] in {"hpm_denial_stub", "control_link_takeover"}


def test_dual_auth_required_for_takeover() -> None:
    no_dual = select_effector(score=0.93, safety_open=True, dual_auth=False)
    with_dual = select_effector(score=0.93, safety_open=True, dual_auth=True)
    assert no_dual["mode"] == "control_link_takeover"
    assert no_dual["authorized"] is False
    assert with_dual["mode"] == "control_link_takeover"
    assert with_dual["authorized"] is True


def test_single_kinetic_entry_present() -> None:
    kinetic = [e for e in EFFECTOR_CATALOG if e.get("kinetic")]
    assert len(kinetic) == 1
    assert kinetic[0]["mode"] == "kamikaze_ram"


def test_kamikaze_gated_by_family_filter() -> None:
    no_kinetic = select_effector(
        score=0.99,
        safety_open=True,
        dual_auth=True,
        enabled_families=(
            "passive",
            "deception",
            "rf_denial",
            "nav_denial",
            "directed_energy_sim",
            "cyber_takeover",
        ),
    )
    assert no_kinetic["mode"] != "kamikaze_ram"
    with_kinetic = select_effector(
        score=0.99,
        safety_open=True,
        dual_auth=True,
        enabled_families=(
            "passive",
            "deception",
            "rf_denial",
            "nav_denial",
            "directed_energy_sim",
            "cyber_takeover",
            "kinetic_ram",
        ),
    )
    assert with_kinetic["mode"] == "kamikaze_ram"
