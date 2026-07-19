import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    share = get_package_share_directory("digital_twin")
    params = os.path.join(share, "config", "digital_twin.yaml")
    return LaunchDescription(
        [
            Node(
                package="digital_twin",
                executable="digital_twin_node",
                name="digital_twin_node",
                output="screen",
                parameters=[params],
            )
        ]
    )
