from pathlib import Path

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def _load_payload_config() -> dict:
    config_path = Path(get_package_share_directory("clearsky_os_bringup")) / "config" / "payload_selector.yaml"
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file) or {}


def _payload_selector_value(path: str, fallback):
    config = _load_payload_config()
    current = config
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return fallback
        current = current[key]
    return current


def _payload_bool(path: str, fallback: bool = False) -> str:
    value = _payload_selector_value(path, fallback)
    return "true" if bool(value) else "false"


def _payload_int(path: str, fallback: int = 1) -> str:
    value = _payload_selector_value(path, fallback)
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return str(fallback)


def _payload_float(path: str, fallback: float) -> str:
    value = _payload_selector_value(path, fallback)
    try:
        return str(float(value))
    except (TypeError, ValueError):
        return str(fallback)


def _include(pkg: str, launch_file: str) -> IncludeLaunchDescription:
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare(pkg), f"/launch/{launch_file}"]),
    )


def _include_if(pkg: str, launch_file: str, condition) -> IncludeLaunchDescription:
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare(pkg), f"/launch/{launch_file}"]),
        condition=condition,
    )


def generate_launch_description() -> LaunchDescription:
    enable_effectors = LaunchConfiguration("enable_effectors")
    enable_effector_sim = LaunchConfiguration("enable_effector_sim")
    enable_cognitive_demo_chain = LaunchConfiguration("enable_cognitive_demo_chain")

    fob_swarm = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("clearsky_os_scout_mothership"), "/launch/fob_swarm.launch.py"]),
        launch_arguments={
            "mesh_enabled": LaunchConfiguration("mesh_motherships_enabled"),
            "fob_count": LaunchConfiguration("fob_count"),
            "micro_capacity_per_fob": LaunchConfiguration("micro_capacity_per_fob"),
            "fob_publish_hz": LaunchConfiguration("fob_coordinator_publish_hz"),
            "mix_sensor_pod": LaunchConfiguration("mix_sensor_pod"),
            "mix_acoustic_disruptor": LaunchConfiguration("mix_acoustic_disruptor"),
            "mix_kevlar_web": LaunchConfiguration("mix_kevlar_web"),
            "mix_cognitive_ew_pod": LaunchConfiguration("mix_cognitive_ew_pod"),
            "mix_kamikaze_ram_slots": LaunchConfiguration("mix_kamikaze_ram_slots"),
            "fob_profile": LaunchConfiguration("fob_profile"),
        }.items(),
    )

    micro_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("clearsky_os_micro_payloads"), "/launch/micro_payloads.launch.py"]
        ),
        condition=IfCondition(LaunchConfiguration("enable_micro_payload_bundle")),
        launch_arguments={
            "mothership_id": LaunchConfiguration("micro_bundle_mothership_id"),
        }.items(),
    )

    effectors_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("clearsky_os_effectors"), "/launch/clearsky_os_effectors.launch.py"]
        ),
        condition=IfCondition(enable_effectors),
        launch_arguments={"enable_effector_sim": enable_effector_sim}.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "mesh_motherships_enabled",
                default_value=_payload_bool("features.mesh_motherships.enabled", True),
            ),
            DeclareLaunchArgument(
                "fob_count",
                default_value=_payload_int("features.mesh_motherships.count", 3),
            ),
            DeclareLaunchArgument(
                "micro_capacity_per_fob",
                default_value=_payload_int("features.micro_capacity_per_fob", 12),
            ),
            DeclareLaunchArgument(
                "fob_coordinator_publish_hz",
                default_value=_payload_float("features.mothership_fob_swarm.coordinator_publish_hz", 1.0),
            ),
            DeclareLaunchArgument(
                "mix_sensor_pod",
                default_value=_payload_int("features.micro_payloads.sensor_pod", 4),
            ),
            DeclareLaunchArgument(
                "mix_acoustic_disruptor",
                default_value=_payload_int("features.micro_payloads.acoustic_disruptor", 2),
            ),
            DeclareLaunchArgument(
                "mix_kevlar_web",
                default_value=_payload_int("features.micro_payloads.kevlar_web", 2),
            ),
            DeclareLaunchArgument(
                "mix_cognitive_ew_pod",
                default_value=_payload_int("features.micro_payloads.cognitive_ew_pod", 3),
            ),
            DeclareLaunchArgument(
                "mix_kamikaze_ram_slots",
                default_value=_payload_int("features.micro_payloads.kamikaze_ram_slots", 1),
            ),
            DeclareLaunchArgument(
                "fob_profile",
                default_value="mothership_fob_standard",
            ),
            DeclareLaunchArgument(
                "enable_micro_payload_bundle",
                default_value=_payload_bool("features.mothership_fob_swarm.enabled", True),
            ),
            DeclareLaunchArgument(
                "micro_bundle_mothership_id",
                default_value="mhs-001",
            ),
            DeclareLaunchArgument(
                "enable_kamikaze_ram_bundle",
                default_value=_payload_bool("features.kamikaze_ram.enabled", False),
            ),
            DeclareLaunchArgument(
                "enable_effectors",
                default_value=_payload_bool("features.effectors.enabled", True),
            ),
            DeclareLaunchArgument(
                "enable_effector_sim",
                default_value=_payload_bool("features.effectors.enable_sim", True),
            ),
            DeclareLaunchArgument(
                "enable_cognitive_demo_chain",
                default_value=_payload_bool("features.cognitive_demo_chain.enabled", True),
            ),
            _include("clearsky_os_sensors", "clearsky_os_sensors.launch.py"),
            _include("clearsky_os_fusion", "clearsky_os_fusion.launch.py"),
            _include("clearsky_os_darkspace_integration", "darkspace_integration.launch.py"),
            _include("clearsky_os_safety_gate", "clearsky_os_safety_gate.launch.py"),
            fob_swarm,
            micro_launch,
            _include("clearsky_os_operator_copilot", "clearsky_os_operator_copilot.launch.py"),
            effectors_launch,
            _include_if("agent_orchestrator", "agent_orchestrator.launch.py", IfCondition(enable_cognitive_demo_chain)),
            _include_if("digital_twin", "digital_twin.launch.py", IfCondition(enable_cognitive_demo_chain)),
            _include_if("cognitive_ew", "cognitive_ew.launch.py", IfCondition(enable_cognitive_demo_chain)),
        ]
    )
