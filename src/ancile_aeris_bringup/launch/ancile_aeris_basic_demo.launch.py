from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


def _include(pkg: str, launch_file: str) -> IncludeLaunchDescription:
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare(pkg), f"/launch/{launch_file}"]),
    )


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            _include("ancile_aeris_sensors", "ancile_aeris_sensors.launch.py"),
            _include("ancile_aeris_fusion", "ancile_aeris_fusion.launch.py"),
            _include("ancile_aeris_darkspace_integration", "darkspace_integration.launch.py"),
            _include("ancile_aeris_safety_gate", "ancile_aeris_safety_gate.launch.py"),
            _include("scout_mothership", "scout_mothership.launch.py"),
            _include("ancile_aeris_operator_copilot", "ancile_aeris_operator_copilot.launch.py"),
        ]
    )
