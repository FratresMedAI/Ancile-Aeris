from pathlib import Path

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare


def _payload_feature_default(feature_name: str, fallback: str = "false") -> str:
    config_path = Path(get_package_share_directory("ancile_aeris_bringup")) / "config" / "payload_selector.yaml"
    if not config_path.exists():
        return fallback

    with config_path.open("r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}
    features = config.get("features", {})
    if not isinstance(features, dict) or feature_name not in features:
        return fallback
    return "true" if bool(features[feature_name]) else "false"


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
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "enable_baby_interceptor",
                default_value=_payload_feature_default("enable_baby_interceptor", "false"),
            ),
            _include("ancile_aeris_sensors", "ancile_aeris_sensors.launch.py"),
            _include("ancile_aeris_fusion", "ancile_aeris_fusion.launch.py"),
            _include("ancile_aeris_darkspace_integration", "darkspace_integration.launch.py"),
            _include("ancile_aeris_safety_gate", "ancile_aeris_safety_gate.launch.py"),
            _include("scout_mothership", "scout_mothership.launch.py"),
            _include("ancile_aeris_operator_copilot", "ancile_aeris_operator_copilot.launch.py"),
            _include_if("baby_interceptor", "baby_interceptor.launch.py", IfCondition(enable_baby_interceptor)),
        ]
    )
