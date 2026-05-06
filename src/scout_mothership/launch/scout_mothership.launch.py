import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share_dir = get_package_share_directory("scout_mothership")
    config_yaml = os.path.join(share_dir, "config", "scout_config.yaml")
    mesh_enabled = LaunchConfiguration("mesh_enabled")
    mesh_peer_count = LaunchConfiguration("mesh_peer_count")
    return LaunchDescription(
        [
            DeclareLaunchArgument("mesh_enabled", default_value="true"),
            DeclareLaunchArgument("mesh_peer_count", default_value="2"),
            Node(
                package="scout_mothership",
                executable="scout_mothership_node",
                name="scout_mothership_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml, {"mesh_enabled": mesh_enabled, "mesh_peer_count": mesh_peer_count}],
            )
        ]
    )
