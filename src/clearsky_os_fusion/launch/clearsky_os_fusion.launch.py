import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share = get_package_share_directory("clearsky_os_fusion")
    params = os.path.join(share, "config", "clearsky_os_fusion.yaml")
    return LaunchDescription(
        [
            Node(
                package="clearsky_os_fusion",
                executable="clearsky_os_fusion_node",
                name="fusion_node",
                output="screen",
                parameters=[params],
                prefix="python3",
            )
        ]
    )
