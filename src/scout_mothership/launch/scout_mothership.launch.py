import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share_dir = get_package_share_directory("scout_mothership")
    config_yaml = os.path.join(share_dir, "config", "scout_config.yaml")
    return LaunchDescription(
        [
            Node(
                package="scout_mothership",
                executable="scout_mothership_node",
                name="scout_mothership_node",
                output="screen",
                prefix="python3",
                parameters=[config_yaml],
            )
        ]
    )
