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
    config_path = Path(get_package_share_directory("ancile_aeris_bringup")) / "config" / "payload_selector.yaml"
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
    enable_baby_interceptor = LaunchConfiguration("enable_baby_interceptor")
    mesh_enabled = LaunchConfiguration("mesh_motherships_enabled")
    mesh_count = LaunchConfiguration("mesh_motherships_count")
    require_double_authorization = LaunchConfiguration("require_double_authorization")

    scout_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("scout_mothership"), "/launch/scout_mothership.launch.py"]),
        launch_arguments={
            "mesh_enabled": mesh_enabled,
            "mesh_peer_count": mesh_count,
        }.items(),
    )
    interceptor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("baby_interceptor"), "/launch/baby_interceptor.launch.py"]),
        condition=IfCondition(enable_baby_interceptor),
        launch_arguments={"require_double_authorization": require_double_authorization}.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "enable_baby_interceptor",
                default_value=_payload_bool("features.baby_interceptor.enabled", False),
            ),
            DeclareLaunchArgument(
                "require_double_authorization",
                default_value=_payload_bool("features.baby_interceptor.require_double_authorization", True),
            ),
            DeclareLaunchArgument(
                "mesh_motherships_enabled",
                default_value=_payload_bool("features.mesh_motherships.enabled", True),
            ),
            DeclareLaunchArgument(
                "mesh_motherships_count",
                default_value=_payload_int("features.mesh_motherships.count", 2),
            ),
            _include("ancile_aeris_sensors", "ancile_aeris_sensors.launch.py"),
            _include("ancile_aeris_fusion", "ancile_aeris_fusion.launch.py"),
            _include("ancile_aeris_darkspace_integration", "darkspace_integration.launch.py"),
            _include("ancile_aeris_safety_gate", "ancile_aeris_safety_gate.launch.py"),
            scout_launch,
            _include("ancile_aeris_operator_copilot", "ancile_aeris_operator_copilot.launch.py"),
            interceptor_launch,
        ]
    )
